// ==== DUMMY DATA (Replace with AJAX or backend data in production) ====
let categories = [
  { id: 1, name: 'Electronics' },
  { id: 2, name: 'Clothes' },
  { id: 3, name: 'Food' }
];
let products = [
  { id: 1, sku: 'EL-001', name: 'Smartphone', category: 'Electronics', cost_price: 200, sell_price: 300, size: '6in', color: 'Black' },
  { id: 2, sku: 'CL-101', name: 'T-shirt', category: 'Clothes', cost_price: 8, sell_price: 16, size: 'M', color: 'White' },
  { id: 3, sku: 'FD-311', name: 'Apple', category: 'Food', cost_price: 1, sell_price: 2, size: '', color: 'Red' }
];
let warehouses = [
  { id: 1, name: 'Main Warehouse', address: '34, First St' },
  { id: 2, name: 'Warehouse 2', address: 'Industrial Zone' }
];

// ==== PRODUCTS ====
function loadProductList() {
  const table = document.getElementById('productTable').querySelector('tbody');
  const searchInput = document.getElementById('prodSearch');
  let filtered = [...products];

  function render(rows) {
    table.innerHTML = rows.length
      ? rows.map((p, idx) => `
        <tr>
          <td>${idx + 1}</td>
          <td>${p.sku}</td>
          <td>${p.name}</td>
          <td>${p.category}</td>
          <td>$${Number(p.cost_price).toFixed(2)}</td>
          <td>$${Number(p.sell_price).toFixed(2)}</td>
          <td>${p.size || '-'}</td>
          <td>${p.color || '-'}</td>
          <td>
            <a href="product_form.html?id=${p.id}" class="table-action">Edit</a>
            <button type="button" onclick="deleteProduct(${p.id})" class="table-action danger">Delete</button>
          </td>
        </tr>
      `).join('')
      : `<tr><td colspan="9" style="text-align:center;color:#888">No products found.</td></tr>`;
  }

  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = products.filter(
      p => p.sku.toLowerCase().includes(val) ||
           p.name.toLowerCase().includes(val) ||
           p.category.toLowerCase().includes(val)
    );
    render(filtered);
  }

  if (searchInput) searchInput.addEventListener('input', filterTable);
  render(filtered);
}

function productFormInit() {
  const form = document.getElementById('productForm');
  if (!form) return;
  const sku = document.getElementById('prodSKU');
  const name = document.getElementById('prodName');
  const categorySel = document.getElementById('prodCategory');
  const costPrice = document.getElementById('prodCostPrice');
  const sellPrice = document.getElementById('prodSellPrice');
  const size = document.getElementById('prodSize');
  const color = document.getElementById('prodColor');
  const skuErr = document.getElementById('prodSKUErr');
  const nameErr = document.getElementById('prodNameErr');
  const catErr = document.getElementById('prodCategoryErr');
  const costErr = document.getElementById('prodCostPriceErr');
  const sellErr = document.getElementById('prodSellPriceErr');

  // Select options to categories
  categorySel.innerHTML = categories.map(c => `<option value="${c.name}">${c.name}</option>`).join('');

  // If editing (has id param)
  const urlParams = new URLSearchParams(window.location.search);
  const editId = urlParams.get('id');
  if (editId) {
    const prod = products.find(p => p.id === Number(editId));
    if (prod) {
      sku.value = prod.sku;
      name.value = prod.name;
      categorySel.value = prod.category;
      costPrice.value = prod.cost_price;
      sellPrice.value = prod.sell_price;
      size.value = prod.size;
      color.value = prod.color;
      document.getElementById('prodFormTitle').innerText = 'Edit Product';
    }
  }

  form.onsubmit = function(e) {
    e.preventDefault();
    [skuErr, nameErr, catErr, costErr, sellErr].forEach(err => err.innerText = '');

    let hasError = false;
    if (!sku.value.trim()) { skuErr.innerText = 'SKU is required'; hasError = true; }
    if (!name.value.trim()) { nameErr.innerText = 'Name is required'; hasError = true; }
    if (!categorySel.value) { catErr.innerText = 'Select category'; hasError = true; }
    if (!costPrice.value || Number(costPrice.value) < 0) { costErr.innerText = 'Enter a valid cost price'; hasError = true; }
    if (!sellPrice.value || Number(sellPrice.value) < 0) { sellErr.innerText = 'Enter a valid sell price'; hasError = true; }

    if (hasError) return false;

    // Add or update product in dummy data (demo)
    if (editId) {
      let idx = products.findIndex(p => p.id === Number(editId));
      if (idx !== -1) {
        products[idx] = {
          ...products[idx],
          sku: sku.value,
          name: name.value,
          category: categorySel.value,
          cost_price: Number(costPrice.value),
          sell_price: Number(sellPrice.value),
          size: size.value,
          color: color.value
        };
      }
    } else {
      let newId = Math.max(...products.map(p => p.id), 0) + 1;
      products.push({
        id: newId,
        sku: sku.value,
        name: name.value,
        category: categorySel.value,
        cost_price: Number(costPrice.value),
        sell_price: Number(sellPrice.value),
        size: size.value,
        color: color.value
      });
    }

    alertSuccess('Product saved (demo)');
    setTimeout(() => window.location = 'product_list.html', 700);
  };
}

function deleteProduct(id) {
  if (confirm('Are you sure you want to delete this product?')) {
    products = products.filter(p => p.id !== id);
    alertSuccess('Product deleted (demo)');
    loadProductList();
  }
}

// ==== CATEGORIES ====
function loadCategoryList() {
  const table = document.getElementById('categoryTable').querySelector('tbody');
  const searchInput = document.getElementById('catSearch');
  let filtered = [...categories];

  function render(rows) {
    table.innerHTML = rows.length
      ? rows.map((cat, idx) => `
        <tr>
          <td>${idx + 1}</td>
          <td>${cat.name}</td>
          <td>
            <a href="category_form.html?id=${cat.id}" class="table-action">Edit</a>
            <button type="button" onclick="deleteCategory(${cat.id})" class="table-action danger">Delete</button>
          </td>
        </tr>
      `).join('')
      : `<tr><td colspan="3" style="text-align:center;color:#888">No categories found.</td></tr>`;
  }

  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = categories.filter(c => c.name.toLowerCase().includes(val));
    render(filtered);
  }

  if (searchInput) searchInput.addEventListener('input', filterTable);
  render(filtered);
}

function categoryFormInit() {
  const form = document.getElementById('categoryForm');
  if (!form) return;
  const nameInput = document.getElementById('catName');
  const nameErr = document.getElementById('catNameErr');
  const urlParams = new URLSearchParams(window.location.search);
  const editId = urlParams.get('id');

  if (editId) {
    const cat = categories.find(c => c.id === Number(editId));
    if (cat) {
      nameInput.value = cat.name;
      document.getElementById('catFormTitle').innerText = 'Edit Category';
    }
  }

  form.onsubmit = function(e) {
    e.preventDefault();
    nameErr.innerText = '';
    if (!nameInput.value.trim()) {
      nameErr.innerText = 'Name required';
      nameInput.focus();
      return false;
    }

    if (editId) {
      let idx = categories.findIndex(c => c.id === Number(editId));
      if (idx !== -1) categories[idx].name = nameInput.value;
    } else {
      let newId = Math.max(...categories.map(c => c.id), 0) + 1;
      categories.push({ id: newId, name: nameInput.value });
    }
    alertSuccess('Category saved (demo)');
    setTimeout(() => window.location = 'category_list.html', 700);
  };
}

function deleteCategory(id) {
  if (confirm('Are you sure you want to delete this category?')) {
    categories = categories.filter(c => c.id !== id);
    alertSuccess('Category deleted (demo)');
    loadCategoryList();
  }
}

// ==== WAREHOUSES ====
function loadWarehouseList() {
  const table = document.getElementById('warehouseTable').querySelector('tbody');
  const searchInput = document.getElementById('whSearch');
  let filtered = [...warehouses];

  function render(rows) {
    table.innerHTML = rows.length
      ? rows.map((wh, idx) => `
        <tr>
          <td>${idx + 1}</td>
          <td>${wh.name}</td>
          <td>${wh.address}</td>
          <td>
            <a href="warehouse_form.html?id=${wh.id}" class="table-action">Edit</a>
            <button type="button" onclick="deleteWarehouse(${wh.id})" class="table-action danger">Delete</button>
          </td>
        </tr>
      `).join('')
      : `<tr><td colspan="4" style="text-align:center;color:#888">No warehouses found.</td></tr>`;
  }

  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = warehouses.filter(
      w => w.name.toLowerCase().includes(val) ||
           (w.address && w.address.toLowerCase().includes(val))
    );
    render(filtered);
  }

  if (searchInput) searchInput.addEventListener('input', filterTable);
  render(filtered);
}

function warehouseFormInit() {
  const form = document.getElementById('warehouseForm');
  if (!form) return;
  const nameInput = document.getElementById('whName');
  const addressInput = document.getElementById('whAddress');
  const nameErr = document.getElementById('whNameErr');
  const urlParams = new URLSearchParams(window.location.search);
  const editId = urlParams.get('id');

  if (editId) {
    const wh = warehouses.find(w => w.id === Number(editId));
    if (wh) {
      nameInput.value = wh.name;
      addressInput.value = wh.address;
      document.getElementById('whFormTitle').innerText = 'Edit Warehouse';
    }
  }

  form.onsubmit = function(e) {
    e.preventDefault();
    nameErr.innerText = '';
    if (!nameInput.value.trim()) {
      nameErr.innerText = 'Name required';
      nameInput.focus();
      return false;
    }

    if (editId) {
      let idx = warehouses.findIndex(w => w.id === Number(editId));
      if (idx !== -1) {
        warehouses[idx].name = nameInput.value;
        warehouses[idx].address = addressInput.value;
      }
    } else {
      let newId = Math.max(...warehouses.map(w => w.id), 0) + 1;
      warehouses.push({ id: newId, name: nameInput.value, address: addressInput.value });
    }

    alertSuccess('Warehouse saved (demo)');
    setTimeout(() => window.location = 'warehouse_list.html', 700);
  };
}

function deleteWarehouse(id) {
  if (confirm('Are you sure you want to delete this warehouse?')) {
    warehouses = warehouses.filter(w => w.id !== id);
    alertSuccess('Warehouse deleted (demo)');
    loadWarehouseList();
  }
}