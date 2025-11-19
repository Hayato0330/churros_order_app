// functions/api/base_price.js

export async function onRequest(context) {
  const { request, env } = context;
  const db = env.PRICING_DB;

  const headers = {
    "Content-Type": "application/json",
  };

  // GET: 現在の基本価格を取得
  if (request.method === "GET") {
    const row = await db
      .prepare("SELECT plain, choco, strawberry FROM base_prices WHERE id = 1")
      .first();

    // 未設定ならデフォルト値を返す（好きな値に変えてよい）
    const plain = row?.plain ?? 300;
    const choco = row?.choco ?? 350;
    const strawberry = row?.strawberry ?? 380;

    return new Response(JSON.stringify({ plain, choco, strawberry }), {
      status: 200,
      headers,
    });
  }

  // POST: 基本価格を保存
  if (request.method === "POST") {
    try {
      const body = await request.json();
      const toInt = (v, fallback = 0) =>
        Number.isFinite(+v) && +v >= 0 ? Math.floor(+v) : fallback;

      const plain = toInt(body.plain, 0);
      const choco = toInt(body.choco, 0);
      const strawberry = toInt(body.strawberry, 0);

      await db
        .prepare(
          `INSERT INTO base_prices (id, plain, choco, strawberry)
           VALUES (1, ?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET
             plain=excluded.plain,
             choco=excluded.choco,
             strawberry=excluded.strawberry`
        )
        .bind(plain, choco, strawberry)
        .run();

      return new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers,
      });
    } catch (e) {
      return new Response(
        JSON.stringify({ ok: false, error: String(e?.message || e) }),
        { status: 400, headers }
      );
    }
  }

  return new Response(JSON.stringify({ ok: false, error: "Method not allowed" }), {
    status: 405,
    headers,
  });
}
