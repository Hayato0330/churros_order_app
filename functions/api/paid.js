// functions/api/paid.js
export async function onRequest(context) {
  const { request, env } = context;
  const db = env.DB;

  // CORS ヘッダ
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://churros-order-admin.pages.dev", // 管理画面のURL
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  // プリフライト対応
  if (request.method === "OPTIONS") {
    return new Response(null, { headers });
  }

  if (request.method !== "POST") {
    return new Response(JSON.stringify({ ok: false, error: "Method not allowed" }), {
      status: 405,
      headers,
    });
  }

  try {
    const body = await request.json();
    const id = Number(body.id);
    if (!Number.isFinite(id) || id <= 0) {
      return new Response(JSON.stringify({ ok: false, error: "Invalid id" }), {
        status: 400,
        headers,
      });
    }

    const result = await db
      .prepare(`UPDATE orders SET paid = 1 WHERE id = ?`)
      .bind(id)
      .run();

    return new Response(
      JSON.stringify({ ok: true, changes: result.meta?.changes ?? 0 }),
      { status: 200, headers }
    );
  } catch (e) {
    return new Response(
      JSON.stringify({ ok: false, error: String(e?.message || e) }),
      { status: 500, headers }
    );
  }
}
