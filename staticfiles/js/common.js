// Load navbar/sidebar partials into every page (if found)
document.addEventListener('DOMContentLoaded', function() {
  function loadPartial(id, file) {
    const el = document.getElementById(id);
    if (el) {
      fetch('/static/partials/' + file)
        .then(r => r.text())
        .then(html => { el.innerHTML = html; });
    }
  }
  loadPartial('navbar', '_navbar.html');
  loadPartial('sidebar', 'sidebar.html');
});

// Universal alert success/error helpers
function alertSuccess(msg) {
  showAlert(msg, "success");
}
function alertError(msg) {
  showAlert(msg, "error");
}
function showAlert(msg, type) {
  let alertDiv = document.createElement("div");
  alertDiv.className = "custom-alert " + type;
  alertDiv.innerText = msg;
  document.getElementById("alert-container")?.appendChild(alertDiv);
  setTimeout(() => alertDiv.remove(), 2300);
}

// Universal modal helpers
function showModal(title, body, footerHtml='') {
  document.getElementById('modalTitle').innerHTML = title;
  document.getElementById('modalBody').innerHTML = body;
  document.getElementById('modalFooter').innerHTML = footerHtml;
  document.getElementById('universalModal').style.display = 'flex';
}
function closeModal() {
  document.getElementById('universalModal').style.display = 'none';
}