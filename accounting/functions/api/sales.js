// async function loadSales() {
//   const date = document.getElementById("sales-date").value;
//   if (!date) return;

//   const res = await fetch(`/api/sales?date=${date}`);
//   const data = await res.json();

//   document.getElementById("basic").textContent = data.basicTotal;
//   document.getElementById("discount").textContent = data.discountTotal;
//   document.getElementById("total").textContent = data.total;
// }

// functions/api/sales.js
// 1日の売上を「基本価格」と「値下げ後」に分けて返す

export async function onRequest(context) {
  const { request, env } = context;

  const headers = { "Content-Type": "application/json" };
  const url = new URL(request.url);
  const date = url.searchParams.get("date"); // "YYYY-MM-DD"

  if (!date) {
    return new Response(
      JSON.stringify({ ok: false, error: "date query is required (YYYY-MM-DD)" }),
      { status: 400, headers }
    );
  }

  try {
    const ordersDb = env.ORDERS_DB;
    const pricingDb = env.PRICING_DB;

    // --- 基本価格 ---
    const baseRow = await pricingDb
      .prepare("SELECT plain, choco, strawberry FROM base_prices WHERE id = 1")
      .first();
    const basePrice = {
      plain: baseRow?.plain ?? 300,
      choco: baseRow?.choco ?? 350,
      strawberry: baseRow?.strawberry ?? 380,
    };

    // --- 価格ルール一覧（値下げルール） ---
    const { results: rules } = await pricingDb
      .prepare(
        "SELECT start_at, plain, choco, strawberry FROM price_rules ORDER BY start_at ASC"
      )
      .all();

    const parsedRules = rules.map((r) => ({
      startAt: new Date(r.start_at),
      plain: r.plain,
      choco: r.choco,
      strawberry: r.strawberry,
    }));

    // --- 指定日の注文一覧 ---
    const startJst = new Date(date + "T00:00:00+09:00");
    const endJst = new Date(date + "T23:59:59.999+09:00");
    const startIsoUtc = startJst.toISOString();
    const endIsoUtc = endJst.toISOString();

    const { results: orders } = await ordersDb
      .prepare(
        `SELECT id, created_at, plain, choco, strawberry
         FROM orders
         WHERE created_at >= ? AND created_at <= ?`
      )
      .bind(startIsoUtc, endIsoUtc)
      .all();

    // --- 集計 ---
    const basicCount = { plain: 0, choco: 0, strawberry: 0 };
    const discountCount = { plain: 0, choco: 0, strawberry: 0 };
    let basicTotal = 0;
    let discountTotal = 0;

    for (const o of orders) {
      const ct = new Date(o.created_at);

      // 適用される価格を決める
      let applied = basePrice;
      let isDiscount = false;

      for (const r of parsedRules) {
        if (r.startAt <= ct) {
          applied = r;
          isDiscount = true;  // 何かしらルールが適用されていれば「値下げ後」とみなす
        } else {
          break;
        }
      }

      if (isDiscount) {
        discountCount.plain += o.plain;
        discountCount.choco += o.choco;
        discountCount.strawberry += o.strawberry;
        discountTotal +=
          o.plain * applied.plain +
          o.choco * applied.choco +
          o.strawberry * applied.strawberry;
      } else {
        basicCount.plain += o.plain;
        basicCount.choco += o.choco;
        basicCount.strawberry += o.strawberry;
        basicTotal +=
          o.plain * applied.plain +
          o.choco * applied.choco +
          o.strawberry * applied.strawberry;
      }
    }

    const total = basicTotal + discountTotal;

    return new Response(
      JSON.stringify({
        ok: true,
        date,
        basic: { count: basicCount, total: basicTotal },
        discount: { count: discountCount, total: discountTotal },
        total,
      }),
      { status: 200, headers }
    );
  } catch (e) {
    return new Response(
      JSON.stringify({ ok: false, error: String(e?.message || e) }),
      { status: 500, headers }
    );
  }
}
