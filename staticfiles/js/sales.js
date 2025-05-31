// ===== DEMO DATA (replace with backend/fetch as needed) =====
let customers = [
  {id: 1, first_name: "Ali", last_name: "Karimov", phone: "+998900011223", address: "Tashkent"},
  {id: 2, first_name: "Matilda", last_name: "Ivanova", phone: "+998911234567", address: "Samarkand"}
];
let salesOrders = [
  {
    id: 1,
    customer: "Ali Karimov",
    cashier: "admin",
    note: "First order",
    date: "2024-04-26",
    total: 300,
    lines: [
      {product: "Smartphone", qty: 1, price: 300, subtotal: 300}
    ]
  }
];
let products = [
  {id: 1, name: "Smartphone", sell_price: 300},
  {id: 2, name: "T-shirt", sell_price: 16}
];

// ===== CUSTOMERS =====
function loadCustomerList() {
  const table = document.getElementById('customerTable').querySelector('tbody');
  const searchInput = document.getElementById('customerSearch');
  let filtered = [...customers];
  function render(rows) {
    table.innerHTML = rows.length ? rows.map((c, idx) => `
      <tr>
        <td>${idx+1}</td>
        <td>${c.first_name}</td>
        <td>${c.last_name}</td>
        <td>${c.phone}</td>
        <td>${c.address}</td>
        <td>
          <a href="customer_form.html?id=${c.id}" class="table-action">Edit</a>
          <button onclick="deleteCustomer(${c.id})" class="table-action danger">Delete</button>
        </td>
      </tr>
    `).join('') : `<tr><td colspan="6" style="text-align:center;color:#888">No customers found.</td></tr>`;
  }
  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = customers.filter(
      c => c.first_name.toLowerCase().includes(val) ||
           c.last_name.toLowerCase().includes(val) ||
           (c.phone && c.phone.toLowerCase().includes(val)) ||
           (c.address && c.address.toLowerCase().includes(val))
    );
    render(filtered);
  }
  searchInput.addEventListener('input', filterTable);
  render(filtered);
}
function customerFormInit() {
  const form = document.getElementById('customerForm');
  const firstName = document.getElementById('custFirstName');
  const lastName = document.getElementById('custLastName');
  const phone = document.getElementById('custPhone');
  const address = document.getElementById('custAddress');
  const firstNameErr = document.getElementById('custFirstNameErr');
  const urlParams = new URLSearchParams(window.location.search);
  const editId = urlParams.get('id');
  if (editId) {
    const c = customers.find(x => x.id === Number(editId));
    if (c) {
      firstName.value = c.first_name;
      lastName.value = c.last_name;
      phone.value = c.phone;
      address.value = c.address;
      document.getElementById('customerFormTitle').innerText = 'Edit Customer';
    }
  }
  form.onsubmit = function(e) {
    e.preventDefault();
    firstNameErr.innerText = '';
    if (!firstName.value.trim()) {
      firstNameErr.innerText = 'First name required';
      firstName.focus();
      return false;
    }
    alertSuccess('Customer saved (demo)');
    setTimeout(() => window.location = 'customer_list.html', 700);
  };
}
function deleteCustomer(id) {
  if (confirm('Are you sure you want to delete this customer?')) {
    customers = customers.filter(c => c.id !== id);
    alertSuccess('Customer deleted (demo)');
    loadCustomerList();
  }
}

// ===== SALES ORDERS =====
function loadOrderList() {
  const table = document.getElementById('orderTable').querySelector('tbody');
  const searchInput = document.getElementById('orderSearch');
  let filtered = [...salesOrders];
  function render(rows) {
    table.innerHTML = rows.length ? rows.map((o, idx) => `
      <tr>
        <td>${idx+1}</td>
        <td>${o.customer}</td>
        <td>${o.cashier}</td>
        <td>$${Number(o.total).toFixed(2)}</td>
        <td>${o.date}</td>
        <td>
          <a href="saleorder_detail.html?id=${o.id}" class="table-action">View</a>
          <a href="saleorder_form.html?id=${o.id}" class="table-action">Edit</a>
          <button onclick="deleteOrder(${o.id})" class="table-action danger">Delete</button>
        </td>
      </tr>
    `).join('') : `<tr><td colspan="6" style="text-align:center;color:#888">No orders found.</td></tr>`;
  }
  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = salesOrders.filter(
      o => o.customer.toLowerCase().includes(val) ||
           o.cashier.toLowerCase().includes(val) ||
           (o.note && o.note.toLowerCase().includes(val))
    );
    render(filtered);
  }
  searchInput.addEventListener('input', filterTable);
  render(filtered);
}
function deleteOrder(id) {
  if (confirm('Are you sure you want to delete this order?')) {
    salesOrders = salesOrders.filter(o => o.id !== id);
    alertSuccess('Order deleted (demo)');
    loadOrderList();
  }
}

// ===== SALES ORDER FORM =====
function saleOrderFormInit() {
  const form = document.getElementById('saleOrderForm');
  const customerSel = document.getElementById('saleCustomer');
  const noteInput = document.getElementById('saleNote');
  const linesDiv = document.getElementById('saleLines');
  const addLineBtn = document.getElementById('addSaleLineBtn');
  const customerErr = document.getElementById('saleCustomerErr');

  // Fill customers
  customerSel.innerHTML = customers.map(
    c => `<option value="${c.id}">${c.first_name} ${c.last_name}</option>`
  ).join('');

  // If editing, load data
  const urlParams = new URLSearchParams(window.location.search);
  const editId = urlParams.get('id');
  let editingLines = [];
  if (editId) {
    const so = salesOrders.find(x => x.id === Number(editId));
    if (so) {
      const cust = customers.find(c => `${c.first_name} ${c.last_name}` === so.customer);
      if (cust) customerSel.value = cust.id;
      noteInput.value = so.note;
      editingLines = so.lines.map(line => ({
        product: products.find(p => p.name === line.product)?.id || "",
        qty: line.qty,
        price: line.price,
        subtotal: line.subtotal
      }));
      document.getElementById('saleOrderFormTitle').innerText = 'Edit Sale Order';
    }
  }

  // Product lines dynamic
  function renderLines() {
    linesDiv.innerHTML = (editingLines.length ? editingLines : [{}]).map((line, idx) => `
      <div class="sale-line" data-idx="${idx}" style="display:flex;gap:7px;margin-bottom:6px;">
        <select class="saleLineProduct" style="width:40%">
          <option value="">Select product</option>
          ${products.map(p =>
            `<option value="${p.id}" ${line.product==p.id?"selected":""}>${p.name}</option>`
          ).join('')}
        </select>
        <input type="number" class="saleLineQty" min="1" value="${line.qty||1}" style="width:20%" required>
        <span class="saleLinePrice" style="width:18%;display:inline-block;">${getProductPrice(line.product)}</span>
        <span class="saleLineSubtotal" style="width:18%;display:inline-block;">${getProductPrice(line.product) * (line.qty||1) || 0}</span>
        <button type="button" onclick="removeSaleLine(${idx})" class="table-action danger" tabindex="-1">&times;</button>
      </div>
    `).join('');
    addLineEvents();
  }
  function getProductPrice(pid) {
    if (!pid) return 0;
    let prod = products.find(p => p.id == pid);
    return prod ? prod.sell_price : 0;
  }
  function addLineEvents() {
    const prods = linesDiv.querySelectorAll('.saleLineProduct');
    const qtys = linesDiv.querySelectorAll('.saleLineQty');
    prods.forEach((prod, idx) => {
      prod.onchange = function() {
        editingLines[idx].product = Number(this.value);
        editingLines[idx].price = getProductPrice(this.value);
        renderLines();
      };
    });
    qtys.forEach((qty, idx) => {
      qty.oninput = function() {
        let val = Math.max(1, Number(this.value));
        editingLines[idx].qty = val;
        editingLines[idx].subtotal = editingLines[idx].price * val;
        renderLines();
      };
    });
  }
  window.removeSaleLine = function(idx) {
    editingLines.splice(idx,1);
    renderLines();
  };
  addLineBtn.onclick = function() {
    editingLines.push({});
    renderLines();
  };

  renderLines();

  form.onsubmit = function(e) {
    e.preventDefault();
    customerErr.innerText = '';
    if (!customerSel.value) {
      customerErr.innerText = 'Select a customer';
      customerSel.focus();
      return false;
    }
    let valid = editingLines.every(l => l.product && l.qty >= 1);
    if (!valid) {
      alertError('Fill all product lines correctly.');
      return false;
    }
    alertSuccess('Sale order saved (demo)');
    setTimeout(() => window.location = 'saleorder_list.html', 700);
  };
}

// ===== ORDER DETAIL =====
function loadOrderDetail() {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get('id');
  const order = salesOrders.find(o => o.id == id);
  if (!order) {
    alertError("Order not found");
    return;
  }
  document.getElementById('orderDetailNum').innerText = "#" + order.id;
  document.getElementById('orderDetailCustomer').innerText = order.customer;
  document.getElementById('orderDetailCashier').innerText = order.cashier;
  document.getElementById('orderDetailDate').innerText = order.date;
  document.getElementById('orderDetailNote').innerText = order.note || '-';
  let table = document.getElementById('orderDetailTable').querySelector('tbody');
  table.innerHTML = order.lines.map((l, idx) => `
    <tr>
      <td>${idx+1}</td>
      <td>${l.product}</td>
      <td>${l.qty}</td>
      <td>$${Number(l.price).toFixed(2)}</td>
      <td>$${Number(l.subtotal).toFixed(2)}</td>
    </tr>
  `).join('');
  document.getElementById('orderDetailTotal').innerText = "$" + Number(order.total).toFixed(2);
}