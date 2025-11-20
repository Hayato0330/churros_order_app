// functions/api/sales.js
// 1日の売上を「基本価格」と「値下げ後」に分けて返すAPI
// ・フロントからは /api/sales?date=YYYY-MM-DD (JSTの日付) で呼ばれる想定
// ・orders.created_at / price_rules.start_at は UTC ISO 文字列として保存されている前提

export async function onRequest(context) {
  const { request, env } = context;
  const ordersDb = env.ORDERS_DB;
  const pricingDb = env.PRICING_DB;

  const headers = { "Content-Type": "application/json" };
  const url = new URL(request.url);
  const date = url.searchParams.get("date"); // "YYYY-MM-DD"（JSTのカレンダー日）

  if (!date) {
    return new Response(
      JSON.stringify({ ok: false, error: "date (YYYY-MM-DD) is required" }),
      { status: 400, headers }
    );
  }

  try {
    // 1. JST のその日 00:00〜23:59:59 を UTC に変換して範囲を作る
    const dayStartJst = new Date(`${date}T00:00:00+09:00`);
    const dayEndJst   = new Date(`${date}T23:59:59.999+09:00`);
    const dayStartUtcIso = dayStartJst.toISOString();
    const dayEndUtcIso   = dayEndJst.toISOString();

    // 2. 基本価格を取得
    const baseRow = await pricingDb
      .prepare("SELECT plain, choco, strawberry FROM base_prices WHERE id = 1")
      .first();

    const basePrice = {
      plain: baseRow?.plain ?? 300,
      choco: baseRow?.choco ?? 350,
      strawberry: baseRow?.strawberry ?? 380,
    };

    // 3. この日の値下げルールだけ取得（JSTの1日内に開始したルール）
    const { results: rules } = await pricingDb
      .prepare(
        `SELECT start_at, plain, choco, strawberry
           FROM price_rules
          WHERE start_at >= ? AND start_at <= ?
          ORDER BY start_at ASC`
      )
      .bind(dayStartUtcIso, dayEndUtcIso)
      .all();

    // 4. この日の注文だけ取得
    const { results: orders } = await ordersDb
      .prepare(
        `SELECT id, created_at, plain, choco, strawberry
           FROM orders
          WHERE created_at >= ? AND created_at <= ?`
      )
      .bind(dayStartUtcIso, dayEndUtcIso)
      .all();

    // 集計用の入れ物
    const basicCount = { plain: 0, choco: 0, strawberry: 0 };
    const discountCount = { plain: 0, choco: 0, strawberry: 0 };
    let basicTotal = 0;
    let discountTotal = 0;

    // 5. 各注文に対して「その時点で有効な一番新しい値下げルール」を探す
    for (const o of orders || []) {
      const orderUtc = new Date(o.created_at); // DBに入っているUTC

      // デフォルトは基本価格
      let appliedPrice = basePrice;
      let isDiscount = false;

      // rules は start_at 昇順になっているので，
      // 「start_at <= created_at」のものを順番に見て，最後に当たったものを採用する
      let appliedRule = null;
      for (const r of rules || []) {
        const ruleUtc = new Date(r.start_at);
        if (ruleUtc <= orderUtc) {
          appliedRule = r;
        } else {
          // これ以降のルールはすべて future なので抜けてよい
          break;
        }
      }

      if (appliedRule) {
        appliedPrice = {
          plain: appliedRule.plain,
          choco: appliedRule.choco,
          strawberry: appliedRule.strawberry,
        };
        isDiscount = true;
      }

      // 小計
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
