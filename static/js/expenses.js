document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('expenseChart')) renderExpenseChart();
  if (document.getElementById('expenseTable')) loadExpenseList();
  if (document.getElementById('categoryTable')) loadCategoryList();
  if (document.getElementById('expenseForm')) expenseFormInit();
  if (document.getElementById('categoryForm')) categoryFormInit();
});

// === Dummy Data ===
let expenseCategories = [
  {id: 1, name: 'Travel', created: '2024-01-03'},
  {id: 2, name: 'Office Supplies', created: '2024-02-20'},
  {id: 3, name: 'Internet', created: '2024-02-25'},
];

let expenses = [
  {id: 1, category: 'Travel', amount: 200, note: 'Taxi', user: 'admin', date: '2024-04-20'},
  {id: 2, category: 'Office Supplies', amount: 38, note: 'Paper', user: 'staff1', date: '2024-05-12'},
  {id: 3, category: 'Internet', amount: 45, note: 'May bill', user: 'admin', date: '2024-05-01'}
];

// === CATEGORY ===
function loadCategoryList() {
  const tbody = document.querySelector('#categoryTable tbody');
  const search = document.getElementById('catSearch');
  const render = (rows) => {
    tbody.innerHTML = rows.map((c, i) => `
      <tr>
        <td>${i+1}</td>
        <td>${c.name}</td>
        <td>${c.created}</td>
        <td class="actions">
          <a href="category_form.html?id=${c.id}" class="btn btn-primary">Edit</a>
          <button onclick="deleteCategory(${c.id})" class="btn btn-danger">Delete</button>
        </td>
      </tr>
    `).join('');
  };
  render(expenseCategories);
  search.addEventListener('input', () => {
    const val = search.value.toLowerCase();
    const filtered = expenseCategories.filter(c => c.name.toLowerCase().includes(val));
    render(filtered);
  });
}

function deleteCategory(id) {
  expenseCategories = expenseCategories.filter(c => c.id !== id);
  alertSuccess("Category deleted");
  loadCategoryList();
}

function categoryFormInit() {
  const form = document.getElementById('categoryForm');
  const name = document.getElementById('catName');
  const err = document.getElementById('catNameErr');
  form.onsubmit = e => {
    e.preventDefault();
    err.innerText = '';
    if (!name.value.trim()) {
      err.innerText = "Name is required";
      return;
    }
    alertSuccess("Category saved");
    setTimeout(() => window.location = 'category_list.html', 700);
  };
}

// === EXPENSE ===
function loadExpenseList() {
  const tbody = document.querySelector('#expenseTable tbody');
  const search = document.getElementById('expenseSearch');
  const render = (rows) => {
    tbody.innerHTML = rows.map((e, i) => `
      <tr>
        <td>${i+1}</td>
        <td>${e.category}</td>
        <td>$${e.amount}</td>
        <td>${e.note}</td>
        <td>${e.user}</td>
        <td>${e.date}</td>
      </tr>
    `).join('');
  };
  render(expenses);
  search.addEventListener('input', () => {
    const val = search.value.toLowerCase();
    const filtered = expenses.filter(e =>
      e.category.toLowerCase().includes(val) ||
      e.note.toLowerCase().includes(val) ||
      e.user.toLowerCase().includes(val)
    );
    render(filtered);
  });
}

function expenseFormInit() {
  const form = document.getElementById('expenseForm');
  const catSel = document.getElementById('expCategory');
  const amount = document.getElementById('expAmount');
  const err = document.getElementById('expAmountErr');

  catSel.innerHTML = expenseCategories.map(c =>
    `<option value="${c.name}">${c.name}</option>`).join('');

  form.onsubmit = e => {
    e.preventDefault();
    err.innerText = '';
    if (!catSel.value) return alertError("Category required");
    if (!amount.value || Number(amount.value) <= 0) {
      err.innerText = "Amount must be > 0";
      return;
    }
    alertSuccess("Expense saved");
    setTimeout(() => window.location = 'expense_list.html', 700);
  };
}

// === CHART ===
function renderExpenseChart() {
  const ctx = document.getElementById('expenseChart').getContext('2d');
  const summary = {};
  expenses.forEach(e => {
    summary[e.category] = (summary[e.category] || 0) + e.amount;
  });

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(summary),
      datasets: [{
        data: Object.values(summary),
        backgroundColor: ['#1fb6ff', '#fbbf24', '#34d399', '#ef4444']
      }]
    },
    options: {
      plugins: {
        legend: { position: 'bottom', labels: { color: '#fff' } }
      }
    }
  });
}

// === ALERTS ===
function alertSuccess(msg) {
  const box = document.createElement("div");
  box.className = "alert";
  box.innerText = msg;
  document.getElementById("alert-container")?.appendChild(box);
  setTimeout(() => box.remove(), 3000);
}

function alertError(msg) {
  const box = document.createElement("div");
  box.className = "alert";
  box.style.color = "#ff4f4f";
  box.style.borderLeftColor = "#ff4f4f";
  box.innerText = msg;
  document.getElementById("alert-container")?.appendChild(box);
  setTimeout(() => box.remove(), 3000);
}