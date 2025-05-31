// ---------- Dummy data (to be replaced with backend fetch/ajax later) ----------
let expenseCategories = [
  {id: 1, name: 'Travel', created: '2024-01-03'},
  {id: 2, name: 'Office Supplies', created: '2024-02-20'},
  {id: 3, name: 'Internet', created: '2024-02-25'},
];
let expenses = [
  {id: 1, category: 'Travel', amount: 200.0, note: 'Taxi', user: 'admin', date: '2024-04-20'},
  {id: 2, category: 'Office Supplies', amount: 37.5, note: 'Paper', user: 'staff1', date: '2024-05-12'},
  {id: 3, category: 'Internet', amount: 45.0, note: 'May bill', user: 'admin', date: '2024-05-01'},
];

// --------------- CATEGORY LIST ---------------
function loadCategoryList() {
  const table = document.getElementById('categoryTable').querySelector('tbody');
  const searchInput = document.getElementById('catSearch');
  let filtered = expenseCategories;

  function render(rows) {
    table.innerHTML = rows.map((cat, idx) => `
      <tr>
        <td>${idx + 1}</td>
        <td>${cat.name}</td>
        <td>${cat.created}</td>
        <td>
          <a href="category_form.html?id=${cat.id}" class="table-action">Edit</a>
          <button onclick="deleteCategory(${cat.id})" class="table-action danger">Delete</button>
        </td>
      </tr>
    `).join('');
  }
  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = expenseCategories.filter(c => c.name.toLowerCase().includes(val));
    render(filtered);
  }
  searchInput.addEventListener('input', filterTable);
  render(filtered);
}

// --------------- CATEGORY FORM ---------------
function categoryFormInit() {
  const form = document.getElementById('categoryForm');
  const nameInput = document.getElementById('catName');
  const nameErr = document.getElementById('catNameErr');
  form.onsubmit = function(e) {
    e.preventDefault();
    nameErr.innerText = '';
    if (!nameInput.value.trim()) {
      nameErr.innerText = 'Name required';
      nameInput.focus();
      return false;
    }
    // Save/update
    alertSuccess('Category saved (demo)');
    setTimeout(() => window.location = 'category_list.html', 700);
  };
}

// Simulate delete (demo)
function deleteCategory(id) {
  if (confirm('Are you sure you want to delete this category?')) {
    expenseCategories = expenseCategories.filter(c => c.id !== id);
    alertSuccess('Category deleted (demo)');
    loadCategoryList();
  }
}

// --------------- EXPENSE LIST ---------------
function loadExpenseList() {
  const table = document.getElementById('expenseTable').querySelector('tbody');
  const searchInput = document.getElementById('expenseSearch');
  let filtered = expenses;

  function render(rows) {
    table.innerHTML = rows.map((exp, idx) => `
      <tr>
        <td>${idx + 1}</td>
        <td>${exp.category}</td>
        <td>$${Number(exp.amount).toFixed(2)}</td>
        <td>${exp.note}</td>
        <td>${exp.user}</td>
        <td>${exp.date}</td>
      </tr>
    `).join('');
  }
  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = expenses.filter(e =>
      e.category.toLowerCase().includes(val) ||
      e.note.toLowerCase().includes(val) ||
      e.user.toLowerCase().includes(val)
    );
    render(filtered);
  }
  searchInput.addEventListener('input', filterTable);
  render(filtered);
}

// --------------- EXPENSE FORM ---------------
function expenseFormInit() {
  const form = document.getElementById('expenseForm');
  const categorySel = document.getElementById('expCategory');
  const amountInput = document.getElementById('expAmount');
  const amountErr = document.getElementById('expAmountErr');
  // Fill categories
  categorySel.innerHTML = expenseCategories.map(c =>
    `<option value="${c.name}">${c.name}</option>`
  ).join('');
  form.onsubmit = function(e) {
    e.preventDefault();
    amountErr.innerText = '';
    if (!categorySel.value) {
      alertError('Category is required!');
      return false;
    }
    if (!amountInput.value || Number(amountInput.value) <= 0) {
      amountErr.innerText = 'Enter a valid amount';
      amountInput.focus();
      return false;
    }
    alertSuccess('Expense saved (demo)');
    setTimeout(() => window.location = 'expense_list.html', 700);
  };
}