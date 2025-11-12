export async function onRequestPost(context) {
  const { request, env } = context;

  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
  if (request.method === "OPTIONS") {
    return new Response(null, { headers: cors });
  }

  try {
    const body = await request.json();
    const toInt = (v) => Number.isFinite(+v) && +v >= 0 ? Math.floor(+v) : 0;

    const plain = toInt(body?.plain);
    const choco = toInt(body?.choco);
    const strawberry = toInt(body?.strawberry);

    const createdAt = new Date().toISOString();
    const served = 0;
    const paid = 0;

    // order_no削除済み → paid追加済みスキーマに対応
    const row = await env.DB
      .prepare(
        `INSERT INTO orders (created_at, plain, choco, strawberry, served, paid)
         VALUES (?, ?, ?, ?, ?, ?)
         RETURNING id`
      )
      .bind(createdAt, plain, choco, strawberry, served, paid)
      .first();

    const insertId = row?.id;

    return new Response(
      JSON.stringify({ ok: true, id: insertId, createdAt }),
      { status: 200, headers: { "Content-Type": "application/json", ...cors } }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ ok: false, error: String(err?.message || err) }),
      { status: 400, headers: { "Content-Type": "application/json", ...cors } }
    );
  }
}
