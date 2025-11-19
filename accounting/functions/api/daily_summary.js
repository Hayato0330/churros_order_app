// functions/api/daily_summary.js

export async function onRequest(context) {
  const { request, env } = context;

  const headers = {
    "Content-Type": "application/json",
  };

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

    // --- 1. 基本価格 ---
    const baseRow = await pricingDb
      .prepare("SELECT plain, choco, strawberry FROM base_prices WHERE id = 1")
      .first();
    const basePrice = {
      plain: baseRow?.plain ?? 300,
      choco: baseRow?.choco ?? 350,
      strawberry: baseRow?.strawberry ?? 380,
    };

    // --- 2. 価格ルール一覧 ---
    const { results: rules } = await pricingDb
      .prepare(
        "SELECT start_at, plain, choco, strawberry FROM price_rules ORDER BY start_at ASC"
      )
      .all();

    // 文字列→Dateに変換しておく
    const parsedRules = rules.map((r) => ({
      startAt: new Date(r.start_at),
      plain: r.plain,
      choco: r.choco,
      strawberry: r.strawberry,
    }));

    // --- 3. 指定日の注文一覧を ORDERS_DB から取得 ---
    // created_at は ISO(UTC) を想定．指定日は日本時間で扱うため +09:00 で境界を決める．
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

    // --- 4. 集計 ---
    let totalPlain = 0;
    let totalChoco = 0;
    let totalStraw = 0;
    let totalAmount = 0;

    for (const o of orders) {
      const ct = new Date(o.created_at);

      // 適用される価格を決める
      let applied = basePrice;
      for (const r of parsedRules) {
        if (r.startAt <= ct) {
          applied = r; // より新しいルールを上書き
        } else {
          break;
        }
      }

      totalPlain += o.plain;
      totalChoco += o.choco;
      totalStraw += o.strawberry;

      totalAmount +=
        o.plain * applied.plain +
        o.choco * applied.choco +
        o.strawberry * applied.strawberry;
    }

    return new Response(
      JSON.stringify({
        ok: true,
        date,
        totalPlain,
        totalChoco,
        totalStrawberry: totalStraw,
        totalAmount,
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
