// ========================================================================
// users.js — Modern Dark Dashboard Logic for Django Templates
// Enhanced with modern animations, better UX, and robust functionality
// ========================================================================

document.addEventListener('DOMContentLoaded', function() {
  // Initialize based on current page
  initializePage();

  // Set up global event listeners
  setupGlobalEvents();

  // Initialize tooltips and animations
  initializeAnimations();
});

/* ------------------------------------------------------------------------
   PAGE INITIALIZATION
------------------------------------------------------------------------- */
function initializePage() {
  // Detect current page and initialize accordingly
  if (document.getElementById('userTable')) {
    initUserListPage();
  }

  if (document.getElementById('userForm')) {
    initUserFormPage();
  }

  if (document.querySelector('.profile-card-modern')) {
    initProfilePage();
  }

  // Initialize search functionality if present
  initializeSearch();

  // Initialize role badge animations
  initializeRoleBadges();
}

/* ------------------------------------------------------------------------
   GLOBAL EVENT LISTENERS
------------------------------------------------------------------------- */
function setupGlobalEvents() {
  // Handle all delete confirmations
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-btn') || e.target.closest('.delete-btn')) {
      e.preventDefault();
      const link = e.target.closest('.delete-btn') || e.target;
      showDeleteConfirmation(link);
    }
  });

  // Handle form submissions with loading states
  document.addEventListener('submit', function(e) {
    if (e.target.tagName === 'FORM') {
      handleFormSubmission(e);
    }
  });

  // Add keyboard navigation
  document.addEventListener('keydown', function(e) {
    handleKeyboardNavigation(e);
  });
}

/* ------------------------------------------------------------------------
   ALERT SYSTEM
------------------------------------------------------------------------- */
function showAlert(message, type = 'success', duration = 4000) {
  const container = getOrCreateAlertContainer();
  const alertId = 'alert_' + Date.now();

  const alertBox = document.createElement('div');
  alertBox.id = alertId;
  alertBox.className = `alert ${type}`;
  alertBox.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between;">
      <span>${message}</span>
      <button onclick="removeAlert('${alertId}')" style="background: none; border: none; color: inherit; cursor: pointer; font-size: 1.2em; padding: 0; margin-left: 12px;">&times;</button>
    </div>
  `;

  container.appendChild(alertBox);

  // Auto remove after duration
  setTimeout(() => removeAlert(alertId), duration);

  // Add entrance animation
  requestAnimationFrame(() => {
    alertBox.style.transform = 'translateX(0)';
    alertBox.style.opacity = '1';
  });
}

function removeAlert(alertId) {
  const alert = document.getElementById(alertId);
  if (alert) {
    alert.style.transform = 'translateX(100%)';
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 300);
  }
}

function getOrCreateAlertContainer() {
  let container = document.getElementById('alert-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'alert-container';
    document.body.appendChild(container);
  }
  return container;
}

/* ------------------------------------------------------------------------
   USER LIST PAGE FUNCTIONALITY
------------------------------------------------------------------------- */
function initUserListPage() {
  // Add hover effects to table rows
  const tableRows = document.querySelectorAll('#userTable tbody tr');
  tableRows.forEach(row => {
    row.addEventListener('mouseenter', function() {
      this.style.transform = 'scale(1.01)';
    });

    row.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1)';
    });
  });

  // Initialize table animations
  animateTableRows();

  // Add loading states to action buttons
  initializeActionButtons();

  // Initialize pagination if present
  initializePagination();
}

function animateTableRows() {
  const rows = document.querySelectorAll('#userTable tbody tr');
  rows.forEach((row, index) => {
    row.style.opacity = '0';
    row.style.transform = 'translateY(20px)';

    setTimeout(() => {
      row.style.transition = 'all 0.3s ease';
      row.style.opacity = '1';
      row.style.transform = 'translateY(0)';
    }, index * 50);
  });
}

function initializeActionButtons() {
  const actionButtons = document.querySelectorAll('.action-btn');
  actionButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      if (!this.classList.contains('delete-btn')) {
        this.innerHTML = '<span class="loading"></span> Loading...';
        this.disabled = true;
      }
    });
  });
}

function initializePagination() {
  const paginationLinks = document.querySelectorAll('.pagination a');
  paginationLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Add loading state to pagination
      this.innerHTML = '<span class="loading"></span>';
    });
  });
}

/* ------------------------------------------------------------------------
   USER FORM PAGE FUNCTIONALITY
------------------------------------------------------------------------- */
function initUserFormPage() {
  const form = document.getElementById('userForm');
  if (!form) return;

  // Add form validation
  setupFormValidation(form);

  // Add input animations
  setupInputAnimations();

  // Handle form title based on context
  updateFormTitle();

  // Add auto-save functionality (optional)
  setupAutoSave(form);
}

function setupFormValidation(form) {
  const inputs = form.querySelectorAll('input, select');

  inputs.forEach(input => {
    // Real-time validation
    input.addEventListener('blur', function() {
      validateField(this);
    });

    input.addEventListener('input', function() {
      clearFieldError(this);
    });
  });

  // Form submission validation
  form.addEventListener('submit', function(e) {
    e.preventDefault();

    if (validateForm(form)) {
      submitForm(form);
    }
  });
}

function validateField(field) {
  const value = field.value.trim();
  const fieldName = field.name;
  let isValid = true;
  let errorMessage = '';

  // Required field validation
  if (field.hasAttribute('required') && !value) {
    isValid = false;
    errorMessage = `${getFieldLabel(field)} is required.`;
  }

  // Specific field validations
  switch (fieldName) {
    case 'username':
      if (value && value.length < 3) {
        isValid = false;
        errorMessage = 'Username must be at least 3 characters long.';
      }
      break;
    case 'phone':
      if (value && !isValidPhone(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid phone number.';
      }
      break;
  }

  if (!isValid) {
    showFieldError(field, errorMessage);
  } else {
    clearFieldError(field);
  }

  return isValid;
}

function validateForm(form) {
  const inputs = form.querySelectorAll('input[required], select[required]');
  let isValid = true;

  inputs.forEach(input => {
    if (!validateField(input)) {
      isValid = false;
    }
  });

  return isValid;
}

function showFieldError(field, message) {
  const errorId = field.id + 'Err';
  let errorElement = document.getElementById(errorId);

  if (!errorElement) {
    errorElement = document.createElement('span');
    errorElement.id = errorId;
    errorElement.className = 'input-error';
    field.parentNode.appendChild(errorElement);
  }

  errorElement.textContent = message