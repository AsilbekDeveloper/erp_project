document.addEventListener('DOMContentLoaded', function () {
  // Oy nomlari
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  // ----------- OYLIK BAR CHART -----------
  const monthlyCtx = document.getElementById('monthlySalesExpenseChart').getContext('2d');
  new Chart(monthlyCtx, {
    type: 'bar',
    data: {
      labels: monthNames,
      datasets: [
        {
          label: 'Sales',
          data: monthlyData,
          backgroundColor: "#2684ff",
          borderRadius: 6,
          maxBarThickness: 28,
        },
        {
          label: 'Expenses',
          data: monthlyExpenses,
          backgroundColor: "#e74c3c",
          borderRadius: 6,
          maxBarThickness: 28,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: value => value.toLocaleString() }
        }
      }
    }
  });

  // ----------- YILLIK LINE CHART -----------
  const yearlyCtx = document.getElementById('yearlySalesExpenseChart').getContext('2d');
  new Chart(yearlyCtx, {
    type: 'line',
    data: {
      labels: yearlyLabels,
      datasets: [
        {
          label: 'Sales',
          data: yearlyData,
          borderColor: "#00d084",
          backgroundColor: "#00d08433",
          fill: true,
          tension: 0.25,
        },
        {
          label: 'Expenses',
          data: yearlyExpenses,
          borderColor: "#e74c3c",
          backgroundColor: "#e74c3c22",
          fill: true,
          tension: 0.25,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: value => value.toLocaleString() }
        }
      }
    }
  });
});