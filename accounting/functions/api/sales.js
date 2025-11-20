// 適用ルール選択部分（これに置き換え）

// 必ず昇順にしておく（INSERT順に依存させない）
rulesForDay.sort((a, b) => a.startAtJst - b.startAtJst);

for (const o of orders || []) {
  const orderUtc = new Date(o.created_at);
  const orderJst = new Date(orderUtc.getTime() + 9 * 60 * 60 * 1000);

  // デフォルトは基本価格
  let appliedPrice = basePrice;
  let isDiscount = false;

  // 「開始時刻 <= 注文時刻」のうち最も遅いルールを採用
  let appliedRule = null;
  for (const r of rulesForDay) {
    if (orderJst >= r.startAtJst) {
      appliedRule = r;
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
