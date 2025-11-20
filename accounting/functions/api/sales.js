// functions/api/sales.js
// 1日の売上を「基本価格」と「値下げ後」に分けて返す
// ・日付指定は JST の YYYY-MM-DD を想定
// ・DB に保存されている時刻は UTC ISO として扱う
// ・集計対象の日の「その日中に start_at がある値下げルール」だけを使う

export async function onRequest(context) {
  const { request, env } = context;
  const ordersDb = env.ORDERS_DB;
  const pricingDb = env.PRICING_DB;

  const headers = { "Content-Type": "application/json" };

  const url = new URL(request.url);
  const date = url.searchParams.get("date"); // "YYYY-MM-DD"

  if (!date) {
    return new Response(
      JSON.stringify({ ok: false, error: "date (YYYY-MM-DD) is required" }),
      { status: 400, headers }
    );
  }

  try {
    // ---- 1. 集計対象日の JST 境界 → UTC ISO に変換 ----
    const dayStartJst = new Date(`${date}T00:00:00+09:00`);
    const dayEndJst   = new Date(`${date}T23:59:59.999+09:00`);
    const dayStartUtcIso = dayStartJst.toISOString();
    const dayEndUtcIso   = dayEndJst.toISOString();

    // ---- 2. 基本価格を取得 ----
    const baseRow = await pricingDb
      .prepare("SELECT plain, choco, strawberry FROM base_prices WHERE id = 1")
      .first();

    const basePrice = {
      plain: baseRow?.plain ?? 300,
      choco: baseRow?.choco ?? 350,
      strawberry: baseRow?.strawberry ?? 380,
    };

    // ---- 3. 値下げルール一覧（全期間）を取得 ----
    const { results: rulesAll } = await pricingDb
      .prepare(
        "SELECT start_at, plain, choco, strawberry FROM price_rules ORDER BY start_at ASC"
      )
      .all();

    // DB の start_at は UTC ISO を想定
    // → いったん JST に変換して、その「日付」が集計対象日に一致するものだけを使う
    const rulesForDay = (rulesAll || [])
      .map(r => {
        const startUtc = new Date(r.start_at);
        const startJst = new Date(startUtc.getTime() + 9 * 60 * 60 * 1000); // +9h
        return {
          startAtUtc: startUtc,
          startAtJst: startJst,
          plain: r.plain,
          choco: r.choco,
          strawberry: r.strawberry,
        };
      })
      .filter(r => {
        // startAtJst が「その日」の 00:00〜23:59:59.999 の範囲にあるものだけ
        return r.startAtJst >= dayStartJst && r.startAtJst <= dayEndJst;
      })
      .sort((a, b) => a.startAtJst - b.startAtJst); // 念のため昇順ソート

    // ---- 4. 指定日の注文一覧を取得（orders.created_at は UTC ISO 想定） ----
    const { results: orders } = await ordersDb
      .prepare(
        `SELECT id, created_at, plain, choco, strawberry
         FROM orders
         WHERE created_at >= ? AND created_at <= ?`
      )
      .bind(dayStartUtcIso, dayEndUtcIso)
      .all();

    // ---- 5. 集計用変数 ----
    const basicCount = { plain: 0, choco: 0, strawberry: 0 };
    const discountCount = { plain: 0, choco: 0, strawberry: 0 };
    let basicTotal = 0;
    let discountTotal = 0;

    // ---- 6. 注文ごとに「その日の値下げルール」の中から適用ルールを決定 ----
    for (const o of orders || []) {
      const orderUtc = new Date(o.created_at);
      const orderJst = new Date(orderUtc.getTime() + 9 * 60 * 60 * 1000); // JST に変換

      // デフォルトは基本価格（値下げなし）
      let appliedPrice = basePrice;
      let isDiscount = false;

      // その日のルールの中で「開始時刻 <= 注文時刻」のうち一番遅いものを探す
      let latestRule = null;
      for (const r of rulesForDay) {
        if (orderJst >= r.startAtJst) {
          latestRule = r;
        } else {
          // 昇順なので、これ以降は全部未来のルール
          break;
        }
      }

      if (latestRule) {
        appliedPrice = {
          plain: latestRule.plain,
          choco: latestRule.choco,
          strawberry: latestRule.strawberry,
        };
        isDiscount = true;
      }

      const subtotal =
        o.plain * appliedPrice.plain +
        o.choco * appliedPrice.choco +
        o.strawberry * appliedPrice.strawberry;

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
