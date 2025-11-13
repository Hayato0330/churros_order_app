// functions/api/orders.js  （注文用プロジェクト側）

export async function onRequest(context) {
  const { env, request } = context;
  const db = env.DB;

  const { results } = await db.prepare(
    `SELECT
       id,
       created_at,
       plain,
       choco,
       strawberry,
       served,
       paid
     FROM orders
     WHERE paid = 0 OR served = 0
     ORDER BY id ASC`
  ).all();

  // ★ 管理画面からのアクセスを許可するCORSヘッダ
  const headers = {
    "Content-Type": "application/json",
    // 本番では admin のURLだけに絞るのがベスト
    // 例: "https://churros-order-admin.pages.dev"
    "Access-Control-Allow-Origin": "https://churros-order-admin.pages.dev",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  // OPTIONS（プリフライト）対応（念のため）
  if (request.method === "OPTIONS") {
    return new Response(null, { headers });
  }

  // JSON は今まで通り「配列だけ」を返す
  return new Response(JSON.stringify(results), {
    status: 200,
    headers,
  });
}
