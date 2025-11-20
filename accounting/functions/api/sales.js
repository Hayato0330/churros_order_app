// functions/api/sales.js
// 1日の売上を，基本価格分と値下げ後分に分けて返す

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

    // --- 値下げルール一覧（start_at 昇順） ---
    const { results: rules } = await pricingDb
      .prepare(
        "SELECT start_at, plain, choco, strawberry FROM price_rules ORDER BY start_at ASC"
      )
      .all();

    const parsedRules = (rules || []).map((r) => ({
      startAt: new Date(r.start_at), // UTC
      plain: r.plain,
      choco: r.choco,
      strawberry: r.strawberry,
    }));

    // --- 指定日の注文一覧 ---
    // created_at は UTC ISO を前提．日付は「日本時間の日付」で集計したいので +09:00 で境界を作る．
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

    // --- 集計用の変数 ---
    const basicCount = { plain: 0, choco: 0, strawberry: 0 };
    const discountCount = { plain: 0, choco: 0, strawberry: 0 };
    let basicTotal = 0;
    let discountTotal = 0;

    for (const o of orders || []) {
      const ct = new Date(o.created_at); // UTC

      // 適用される価格を決める
      // デフォルトは基本価格
      let applied = basePrice;
      let isDiscount = false;

      // ルールは start_at 昇順に並んでいる想定
      // 「値下げ価格の適用時間より前の注文 → 基本」
      // 「適用時間以降の注文 → その時点で最新の値下げ価格」
      for (const r of parsedRules) {
        if (ct >= r.startAt) {
          applied = r;
          isDiscount = true;
        } else {
          // これ以降のルールは未来なので見ない
          break;
        }
      }

      const sub =
        o.plain * applied.plain +
        o.choco * applied.choco +
        o.strawberry * applied.strawberry;

      if (isDiscount) {
        // 値下げ後エリア
        discountCount.plain += o.plain;
        discountCount.choco += o.choco;
        discountCount.strawberry += o.strawberry;
        discountTotal += sub;
      } else {
        // 値下げ前（基本価格）エリア
        basicCount.plain += o.plain;
        basicCount.choco += o.choco;
        basicCount.strawberry += o.strawberry;
        basicTotal += sub;
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
