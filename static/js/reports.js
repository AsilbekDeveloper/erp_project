document.addEventListener('DOMContentLoaded', function() {
  initializeCharts();
  animateCounters();
});

// Initialize charts function
function initializeCharts() {
  // Monthly Chart
  const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
  new Chart(monthlyCtx, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [
        {
          label: 'Revenue',
          data: monthlyData.sales || [18500, 22300, 19800, 25600, 31200, 28900, 33400, 29800, 35200, 41600, 38900, 42300],
          backgroundColor: 'rgba(102, 126, 234, 0.8)',
          borderColor: 'rgba(102, 126, 234, 1)',
          borderWidth: 2,
          borderRadius: 8,
          borderSkipped: false,
        },
        {
          label: 'Expenses',
          data: monthlyData.expenses || [12400, 15600, 13200, 17800, 21400, 19300, 22800, 20100, 24600, 28200, 26400, 29800],
          backgroundColor: 'rgba(239, 68, 68, 0.8)',
          borderColor: 'rgba(239, 68, 68, 1)',
          borderWidth: 2,
          borderRadius: 8,
          borderSkipped: false,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: { size: 12, weight: '600' }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 11, weight: '500' } }
        },
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          ticks: {
            font: { size: 11 },
            callback: function(value) {
              return '$' + (value / 1000) + 'K';
            }
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  });

  // Yearly Chart
  const yearlyCtx = document.getElementById('yearlyChart').getContext('2d');
  new Chart(yearlyCtx, {
    type: 'line',
    data: {
      labels: yearlyData.labels || ['2020', '2021', '2022', '2023', '2024'],
      datasets: [
        {
          label: 'Revenue',
          data: yearlyData.sales || [156000, 189000, 234000, 287000, 312000],
          borderColor: 'rgba(16, 185, 129, 1)',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgba(16, 185, 129, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 3,
          pointRadius: 6,
          pointHoverRadius: 8,
        },
        {
          label: 'Expenses',
          data: yearlyData.expenses || [108000, 126000, 152000, 184000, 201000],
          borderColor: 'rgba(239, 68, 68, 1)',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgba(239, 68, 68, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 3,
          pointRadius: 6,
          pointHoverRadius: 8,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: { size: 12, weight: '600' }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 11, weight: '500' } }
        },
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0, 0, 0, 0.05)' },
          ticks: {
            font: { size: 11 },
            callback: function(value) {
              return '$' + (value / 1000) + 'K';
            }
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  });
}

// Download report function
function downloadReport() {
  document.getElementById('loadingSpinner').style.display = 'block';

  // Simulate download process
  setTimeout(() => {
    document.getElementById('loadingSpinner').style.display = 'none';

    // Create and download CSV
    const csvContent = generateCSVReport();
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'analytics-report-' + new Date().toISOString().split('T')[0] + '.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }, 1500);
}

// Generate CSV report function
function generateCSVReport() {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  let csv = 'Month,Revenue,Expenses,Net Profit\n';

  const salesData = monthlyData.sales || [18500, 22300, 19800, 25600, 31200, 28900, 33400, 29800, 35200, 41600, 38900, 42300];
  const expensesData = monthlyData.expenses || [12400, 15600, 13200, 17800, 21400, 19300, 22800, 20100, 24600, 28200, 26400, 29800];

  months.forEach((month, index) => {
    const revenue = salesData[index];
    const expenses = expensesData[index];
    const profit = revenue - expenses;
    csv += `${month},${revenue},${expenses},${profit}\n`;
  });

  return csv;
}

// Animate counters function
function animateCounters() {
  const counters = document.querySelectorAll('.metric-value');
  counters.forEach(counter => {
    counter.style.animation = 'fadeInUp 0.8s ease forwards';
  });
}

// Update KPI values function (agar backend dan data kelsa)
function updateKPIValues() {
  // Total Revenue
  const totalRevenueEl = document.getElementById('totalRevenue');
  if (totalRevenueEl && monthlyData.sales) {
    const totalRevenue = monthlyData.sales.reduce((sum, val) => sum + val, 0);
    totalRevenueEl.textContent = '$' + totalRevenue.toLocaleString();
  }

  // Growth rate calculation
  const growthRateEl = document.getElementById('growthRate');
  if (growthRateEl && yearlyData.sales && yearlyData.sales.length >= 2) {
    const currentYear = yearlyData.sales[yearlyData.sales.length - 1];
    const previousYear = yearlyData.sales[yearlyData.sales.length - 2];
    const growthRate = ((currentYear - previousYear) / previousYear * 100).toFixed(1);
    growthRateEl.textContent = '+' + growthRate + '%';
  }

  // Net Profit calculation
  const netProfitEl = document.getElementById('netProfit');
  if (netProfitEl && monthlyData.sales && monthlyData.expenses) {
    const totalRevenue = monthlyData.sales.reduce((sum, val) => sum + val, 0);
    const totalExpenses = monthlyData.expenses.reduce((sum, val) => sum + val, 0);
    const netProfit = totalRevenue - totalExpenses;
    netProfitEl.textContent = '$' + netProfit.toLocaleString();
  }
}