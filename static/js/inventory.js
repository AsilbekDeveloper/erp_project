// === Product List ===
function loadProducts() {
  const tableBody = document.querySelector("#productTable tbody");
  const searchInput = document.getElementById("prodSearch");

  function render(products) {
    tableBody.innerHTML = products.length
      ? products.map((p, i) => `
        <tr>
          <td>${i + 1}</td>
          <td>${p.sku}</td>
          <td>${p.name}</td>
          <td>${p.category}</td>
          <td>$${p.cost_price}</td>
          <td>$${p.sell_price}</td>
          <td>${p.size || "-"}</td>
          <td>${p.color || "-"}</td>
          <td class="actions">
            <a href="product_form.html?id=${p.id}" class="btn btn-primary">Edit</a>
            <button onclick="deleteProduct(${p.id})" class="btn btn-danger">Delete</button>
          </td>
        </tr>
      `).join("")
      : `<tr><td colspan="9" style="text-align:center;">No products found</td></tr>`;
  }

  if (searchInput) {
    searchInput.addEventListener("input", e => {
      const q = e.target.value.toLowerCase();
      const filtered = products.filter(p =>
        p.sku.toLowerCase().includes(q) ||
        p.name.toLowerCase().includes(q) ||
        p.category.toLowerCase().includes(q)
      );
      render(filtered);
    });
  }

  render(products);
}

function deleteProduct(id) {
  if (confirm("Are you sure to delete this product?")) {
    products = products.filter(p => p.id !== id);
    loadProducts();
  }
}

// === Product Form ===
function initProductForm() {
  const form = document.getElementById("productForm");
  if (!form) return;

  const sku = form.querySelector("#prodSKU");
  const name = form.querySelector("#prodName");
  const cat = form.querySelector("#prodCategory");
  const cost = form.querySelector("#prodCostPrice");
  const sell = form.querySelector("#prodSellPrice");

  const idParam = new URLSearchParams(window.location.search).get("id");
  if (idParam) {
    const prod = products.find(p => p.id == idParam);
    if (prod) {
      sku.value = prod.sku;
      name.value = prod.name;
      cat.value = prod.category;
      cost.value = prod.cost_price;
      sell.value = prod.sell_price;
    }
  }

  form.addEventListener("submit", e => {
    e.preventDefault();
    if (!sku.value || !name.value || !cat.value) {
      alert("Please fill in required fields");
      return;
    }

    if (idParam) {
      let index = products.findIndex(p => p.id == idParam);
      products[index] = {
        id: idParam,
        sku: sku.value,
        name: name.value,
        category: cat.value,
        cost_price: cost.value,
        sell_price: sell.value
      };
    } else {
      const newId = Math.max(...products.map(p => p.id)) + 1;
      products.push({
        id: newId,
        sku: sku.value,
        name: name.value,
        category: cat.value,
        cost_price: cost.value,
        sell_price: sell.value
      });
    }

    alert("Saved!");
    window.location = "product_list.html";
  });
}

// === Category/Warehouse Functions ===
// loadCategories(), loadWarehouses(), etc – exactly same structure as above