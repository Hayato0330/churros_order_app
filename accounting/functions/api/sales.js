// functions/api/sales.js
// 1日の売上を「基本価格」と「値下げ後」に分けて返す
// UTC / JST のズレで誤判定が起きないように、比較はすべて JST に統一

export async function onRequest(context) {
  const { request, env } = context;
  const ordersDb = env.ORDERS_DB;
  const pricingDb = env.PRICING_DB;

  const headers = { "Content-Type": "application/json" };

  const url = new URL(request.url);
  const date = url.searchParams.get("date"); // YYYY-MM-DD (JST想定)
  if (!date) {
    return new Response(
      JSON.stringify({ ok: false, error: "date (YYYY-MM-DD) is required" }),
      { status: 400, headers }
    );
  }

  try {
    // ----- JST の 1日の境界を UTC ISO に変換 -----
    const startJst = new Date(`${date}T00:00:00+09:00`);
    const endJst = new Date(`${date}T23:59:59.999+09:00`);
    const startIsoUtc = startJst.toISOString();
    const endIsoUtc = endJst.toISOString();

    // ----- 基本価格を取得 -----
    const baseRow = await pricingDb
      .prepare("SELECT plain, choco, strawberry FROM base_prices WHERE id = 1")
      .first();
    const basePrice = {
      plain: baseRow?.plain ?? 300,
      choco: baseRow?.choco ?? 350,
      strawberry: baseRow?.strawberry ?? 380,
    };

    // ----- 値下げルール（start_at 昇順） -----
    const { results: rules } = await pricingDb
      .prepare(
        "SELECT start_at, plain, choco, strawberry FROM price_rules ORDER BY start_at ASC"
      )
      .all();

    const parsedRules = (rules || []).map(r => ({
      startAtUtc: new Date(r.start_at), // DBはUTCとして扱う
      startAtJst: new Date(new Date(r.start_at).getTime() + 9 * 60 * 60 * 1000), // JST変換
      plain: r.plain,
      choco: r.choco,
      strawberry: r.strawberry,
    }));

    // ----- 指定日の注文一覧 -----
    const { results: orders } = await ordersDb
      .prepare(
        `SELECT id, created_at, plain, choco, strawberry
         FROM orders
         WHERE created_at >= ? AND created_at <= ?`
      )
      .bind(startIsoUtc, endIsoUtc)
      .all();

    // ----- 集計用変数 -----
    const basicCount = { plain: 0, choco: 0, strawberry: 0 };
    const discountCount = { plain: 0, choco: 0, strawberry: 0 };
    let basicTotal = 0;
    let discountTotal = 0;

    // ----- 注文ごとに、適用する価格帯を判定 -----
    for (const o of orders || []) {
      const utcOrder = new Date(o.created_at);
      const jstOrder = new Date(utcOrder.getTime() + 9 * 60 * 60 * 1000);

      // デフォルトは基本価格
      let applied = basePrice;
      let isDiscount = false;
      let latestRule = null;

      // 「値下げ開始 <= 注文」のうち、最も遅いルールだけ使う
      for (const r of parsedRules) {
        if (jstOrder >= r.startAtJst) {
          latestRule = r; // 候補を更新
        }
      }

      if (latestRule) {
        applied = {
          plain: latestRule.plain,
          choco: latestRule.choco,
          strawberry: latestRule.strawberry,
        };
        isDiscount = true;
      }

      // 合計金額
      const subtotal =
        o.plain * applied.plain +
        o.choco * applied.choco +
        o.strawberry * applied.strawberry;

      if (isDiscount) {
        discountCount.plain += o.plain;
        discountCount.choco += o.choco;
        discountCount.strawberry += o.strawberry;
        discountTotal += subtotal;
      } else {
        basicCount.plain += o.plain;
        basicCount.choco += o.choco;
        basicCount.strawberry += o.strawberry;
        basicTotal += subtotal;
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
