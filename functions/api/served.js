export async function onRequestPost(context) {
  const db = context.env.DB;
  const req = await context.request.json();

  await db.prepare(
    `UPDATE orders SET served = 1 WHERE id = ?`
  ).bind(req.id).run();

  return Response.json({ ok: true });
}
