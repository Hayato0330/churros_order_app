export async function onRequest(context) {
  const db = context.env.DB;

  const { results } = await db.prepare(
    `SELECT * FROM orders 
     WHERE paid = 0 OR served = 0
     ORDER BY id ASC`
  ).all();

  return Response.json(results);
}
