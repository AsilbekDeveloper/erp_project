document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("orderTable")) loadOrderList();
  if (document.getElementById("customerTable")) loadCustomerList();
  if (document.getElementById("saleOrderForm")) saleOrderFormInit();
  if (document.getElementById("orderDetailTable")) loadOrderDetail();
});

// === ALERTS ===
function alertSuccess(msg) {
  const box = document.createElement("div");
  box.className = "alert";
  box.textContent = msg;
  document.getElementById("alert-container").appendChild(box);
  setTimeout(() => box.remove(), 3000);
}

function alertError(msg) {
  const box = document.createElement("div");
  box.className = "alert";
  box.style.borderLeftColor = "#f85149";
  box.style.color = "#f85149";
  box.textContent = msg;
  document.getElementById("alert-container").appendChild(box);
  setTimeout(() => box.remove(), 4000);
}

// === DUMMY DATA ===
let customers = [
  {id: 1, first_name: "Ali", last_name: "Karimov", phone: "99890...", address: "Tashkent"},
  {id: 2, first_name: "Matilda", last_name: "Ivanova", phone: "99891...", address: "Samarkand"}
];
let salesOrders = [
  {
    id: 1,
    customer: "Ali Karimov",
    cashier: "admin",
    total: 450,
    date: "2025-05-30",
    lines: [{product: "Smartphone", qty: 1, price: 450, subtotal: 450}],
    note: "Online order"
  }
];
let products = [
  {id: 1, name: "Smartphone", sell_price: 450},
  {id: 2, name: "Headphones", sell_price: 75}
];

// === LOAD ORDER LIST ===
function loadOrderList() {
  const tbody = document.querySelector("#orderTable tbody");
  const search = document.getElementById("orderSearch");
  function render(list) {
    tbody.innerHTML = list.length ? list.map((o, i) => `
      <tr>
        <td>${i+1}</td>
        <td>${o.customer}</td>
        <td>${o.cashier}</td>
        <td>$${o.total}</td>
        <td>${o.date}</td>
        <td class="actions">
          <a href="saleorder_detail.html?id=${o.id}" class="btn btn-primary">View</a>
          <button onclick="deleteOrder(${o.id})" class="btn btn-danger">Delete</button>
        </td>
      </tr>
    `).join("") : `<tr><td colspan="6" style="text-align:center;">No orders found</td></tr>`;
  }

  render(salesOrders);
  search?.addEventListener("input", e => {
    const q = e.target.value.toLowerCase();
    const f = salesOrders.filter(o =>
      o.customer.toLowerCase().includes(q) ||
      o.cashier.toLowerCase().includes(q)
    );
    render(f);
  });
}

function deleteOrder(id) {
  salesOrders = salesOrders.filter(o => o.id !== id);
  alertSuccess("Order deleted");
  loadOrderList();
}

// === ORDER DETAIL ===
function loadOrderDetail() {
  const id = new URLSearchParams(window.location.search).get("id");
  const order = salesOrders.find(o => o.id == id);
  if (!order) return alertError("Order not found");

  document.getElementById("orderDetailNum").textContent = `#${order.id}`;
  document.getElementById("orderDetailCustomer").textContent = order.customer;
  document.getElementById("orderDetailCashier").textContent = order.cashier;
  document.getElementById("orderDetailDate").textContent = order.date;
  document.getElementById("orderDetailNote").textContent = order.note;

  const tbody = document.querySelector("#orderDetailTable tbody");
  tbody.innerHTML = order.lines.map((l, i) => `
    <tr>
      <td>${i+1}</td>
      <td>${l.product}</td>
      <td>${l.qty}</td>
      <td>$${l.price}</td>
      <td>$${l.subtotal}</td>
    </tr>
  `).join("");
  document.getElementById("orderDetailTotal").textContent = `$${order.total}`;
}