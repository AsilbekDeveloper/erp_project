// ===== DEMO DATA (replace with backend/fetch as needed) =====
let users = [
  {id: 1, username: "superadmin", first_name: "Ali", last_name: "Karimov", role: "SUPERADMIN", phone: "+998900011223"},
  {id: 2, username: "manager", first_name: "Matilda", last_name: "Ivanova", role: "ADMIN", phone: "+998911234567"},
  {id: 3, username: "staff", first_name: "John", last_name: "Doe", role: "STAFF", phone: "+998933331212"}
];

// ===== USER LIST =====
function loadUserList() {
  const table = document.getElementById('userTable').querySelector('tbody');
  const searchInput = document.getElementById('userSearch');
  let filtered = [...users];
  function render(rows) {
    table.innerHTML = rows.length ? rows.map((u, idx) => `
      <tr>
        <td>${idx+1}</td>
        <td>${u.username}</td>
        <td>${u.first_name} ${u.last_name}</td>
        <td><span class="role-badge">${formatRole(u.role)}</span></td>
        <td>${u.phone||''}</td>
        <td>
          <a href="user_form.html?id=${u.id}" class="table-action">Edit</a>
          <button onclick="deleteUser(${u.id})" class="table-action danger">Delete</button>
        </td>
      </tr>
    `).join('') : `<tr><td colspan="6" style="text-align:center;color:#888">No users found.</td></tr>`;
  }
  function filterTable() {
    const val = searchInput.value.toLowerCase();
    filtered = users.filter(
      u => u.username.toLowerCase().includes(val) ||
           u.first_name.toLowerCase().includes(val) ||
           u.last_name.toLowerCase().includes(val) ||
           (u.phone && u.phone.toLowerCase().includes(val)) ||
           (u.role && u.role.toLowerCase().includes(val))
    );
    render(filtered);
  }
  searchInput.addEventListener('input', filterTable);
  render(filtered);
}
function formatRole(role) {
  if (role === "SUPERADMIN") return "Super Admin";
  if (role === "ADMIN") return "Admin";
  if (role === "STAFF") return "Staff";
  return role;
}
function deleteUser(id) {
  if (confirm('Are you sure you want to delete this user?')) {
    users = users.filter(u => u.id !== id);
    alertSuccess('User deleted (demo)');
    loadUserList();
  }
}

// ===== USER FORM =====
function userFormInit() {
  const form = document.getElementById('userForm');
  const username = document.getElementById('username');
  const firstName = document.getElementById('firstName');
  const lastName = document.getElementById('lastName');
  const role = document.getElementById('role');
  const phone = document.getElementById('phone');
  const usernameErr = document.getElementById('usernameErr');
  const roleErr = document.getElementById('roleErr');
  const urlParams = new URLSearchParams(window.location.search);
  const editId = urlParams.get('id');
  if (editId) {
    const u = users.find(x => x.id === Number(editId));
    if (u) {
      username.value = u.username;
      firstName.value = u.first_name;
      lastName.value = u.last_name;
      role.value = u.role;
      phone.value = u.phone;
      document.getElementById('userFormTitle').innerText = 'Edit User';
    }
  }
  form.onsubmit = function(e) {
    e.preventDefault();
    usernameErr.innerText = '';
    roleErr.innerText = '';
    if (!username.value.trim()) {
      usernameErr.innerText = 'Username required';
      username.focus();
      return false;
    }
    if (!role.value) {
      roleErr.innerText = 'Role required';
      role.focus();
      return false;
    }
    alertSuccess('User saved (demo)');
    setTimeout(() => window.location = 'user_list.html', 700);
  };
}

// ===== PROFILE (for demo) =====
function loadProfile() {
  // For demo, use the first user as profile
  const u = users[0];
  document.getElementById('profileName').innerText = `${u.first_name} ${u.last_name}`;
  document.getElementById('profileUsername').innerText = u.username;
  document.getElementById('profileRole').innerText = formatRole(u.role);
  document.getElementById('profilePhone').innerText = u.phone;
}