// functions/api/price_rules.js

export async function onRequest(context) {
  const { request, env } = context;
  const db = env.PRICING_DB;

  const headers = {
    "Content-Type": "application/json",
  };

  const url = new URL(request.url);
  const latest = url.searchParams.get("latest");

  // GET
  if (request.method === "GET") {
    // latest=1 のときは「直近1件だけ」返す
    if (latest === "1") {
      const row = await db
        .prepare(
          "SELECT id, start_at, plain, choco, strawberry, note FROM price_rules ORDER BY start_at DESC LIMIT 1"
        )
        .first();

      // まだ値下げが1件もない場合は null を返す
      return new Response(JSON.stringify(row ?? null), {
        status: 200,
        headers,
      });
    }

    // 通常は一覧を配列で返す
    const { results } = await db
      .prepare(
        "SELECT id, start_at, plain, choco, strawberry, note FROM price_rules ORDER BY start_at ASC"
      )
      .all();

    return new Response(JSON.stringify(results), { status: 200, headers });
  }

  // POST: 価格ルールを登録
  if (request.method === "POST") {
    try {
      const body = await request.json();
      const toInt = (v, fallback = 0) =>
        Number.isFinite(+v) && +v >= 0 ? Math.floor(+v) : fallback;

      const start_at = String(body.start_at || "");
      if (!start_at) {
        return new Response(
          JSON.stringify({ ok: false, error: "start_at is required" }),
          { status: 400, headers }
        );
      }

      const plain = toInt(body.plain, 0);
      const choco = toInt(body.choco, 0);
      const strawberry = toInt(body.strawberry, 0);
      const note = String(body.note || "");

      await db
        .prepare(
          `INSERT INTO price_rules (start_at, plain, choco, strawberry, note)
           VALUES (?, ?, ?, ?, ?)`
        )
        .bind(start_at, plain, choco, strawberry, note)
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
