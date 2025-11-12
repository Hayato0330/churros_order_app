// functions/api/order.js
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

    const orderNo = crypto.randomUUID();
    const createdAt = new Date().toISOString();
    const served = 0;

    // ← 挿入して last_rowid を取得
    const result = await env.DB
      .prepare(
        `INSERT INTO orders (order_no, created_at, plain, choco, strawberry, served)
         VALUES (?, ?, ?, ?, ?, ?)`
      )
      .bind(orderNo, createdAt, plain, choco, strawberry, served)
      .run();

    const insertId = result?.meta?.last_rowid; // ← ここが新規ID

    return new Response(
      JSON.stringify({ ok: true, id: insertId, orderNo, createdAt }),
      { status: 200, headers: { "Content-Type": "application/json", ...cors } }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ ok: false, error: String(err?.message || err) }),
      { status: 400, headers: { "Content-Type": "application/json", ...cors } }
    );
  }
}
