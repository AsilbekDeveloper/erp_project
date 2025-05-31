// Modal ochish
document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.getElementById("addCategoryBtn");
  const modal = document.getElementById("addCatModal");
  const closeBtn = document.getElementById("closeCatModal");
  const saveBtn = document.getElementById("saveNewCat");
  const nameInput = document.getElementById("newCatName");
  const errorDiv = document.getElementById("catAddErr");
  const catSelect = document.getElementById("id_category");

  if (!addBtn || !modal || !closeBtn || !saveBtn || !nameInput || !catSelect) return;

  // Modal ochiladi
  addBtn.onclick = function () {
    modal.style.display = "flex";
    errorDiv.innerText = "";
    nameInput.value = "";
    nameInput.focus();
  };

  // Modal yopiladi
  closeBtn.onclick = function () {
    modal.style.display = "none";
    errorDiv.innerText = "";
    nameInput.value = "";
  };

  // Modal tashqarisiga bosilsa ham yopiladi
  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
      errorDiv.innerText = "";
      nameInput.value = "";
    }
  };

  // AJAX orqali kategoriya qo‘shish
  saveBtn.onclick = function () {
    const name = nameInput.value.trim();
    if (!name) {
      errorDiv.innerText = "Category name required!";
      nameInput.focus();
      return;
    }
    // CSRF olish uchun yordamchi funksiya
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";").map(c => c.trim());
        for (let cookie of cookies) {
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    fetch("/inventory/categories/ajax/add/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: "name=" + encodeURIComponent(name),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          // Select ga yangi kategoriya qo‘shish va tanlash
          let opt = document.createElement("option");
          opt.value = data.id;
          opt.text = data.name;
          catSelect.appendChild(opt);
          catSelect.value = data.id;
          modal.style.display = "none";
          errorDiv.innerText = "";
          nameInput.value = "";
        } else {
          errorDiv.innerText = data.error || "Error";
        }
      })
      .catch(() => {
        errorDiv.innerText = "Network error!";
      });
  };
});