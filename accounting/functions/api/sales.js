async function loadSales() {
  const date = document.getElementById("sales-date").value;
  if (!date) return;

  const res = await fetch(`/api/sales?date=${date}`);
  const data = await res.json();

  document.getElementById("basic").textContent = data.basicTotal;
  document.getElementById("discount").textContent = data.discountTotal;
  document.getElementById("total").textContent = data.total;
}
