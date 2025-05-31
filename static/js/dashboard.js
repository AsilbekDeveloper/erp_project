document.addEventListener('DOMContentLoaded', () => {
  const { product_cnt, stock, year_total_sales, year, pie_labels, pie_data, months, bar_rev, bar_cost, line_profit } = backendData;

  document.getElementById('productCnt').textContent = product_cnt;
  document.getElementById('stockCnt').textContent = stock;
  document.getElementById('totalSales').textContent = year_total_sales.toLocaleString();

  const yearSelect = document.getElementById('yearSelect');
  const currentYear = new Date().getFullYear();
  for (let y = currentYear - 4; y <= currentYear; y++) {
    const opt = document.createElement('option');
    opt.value = y;
    opt.textContent = y;
    if (y === year) opt.selected = true;
    yearSelect.appendChild(opt);
  }

  new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
      labels: pie_labels,
      datasets: [{
        data: pie_data,
        backgroundColor: [
          '#00b4d8', '#0077b6', '#90e0ef', '#caf0f8',
          '#4361ee', '#f72585', '#3a0ca3', '#7209b7'
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#e0e6ed',
            font: { size: 12 }
          }
        }
      }
    }
  });

  new Chart(document.getElementById('barLineChart'), {
    data: {
      labels: months,
      datasets: [
        {
          type: 'bar',
          label: 'Revenue',
          data: bar_rev,
          backgroundColor: '#00b4d8',
          yAxisID: 'y'
        },
        {
          type: 'bar',
          label: 'Cost',
          data: bar_cost,
          backgroundColor: '#ffb703',
          yAxisID: 'y'
        },
        {
          type: 'line',
          label: 'Profit',
          data: line_profit,
          borderColor: '#8ecae6',
          backgroundColor: '#8ecae655',
          yAxisID: 'y',
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: '#8ecae6'
        }
      ]
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: '#e0e6ed'
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: '#e0e6ed' },
          grid: { color: '#324a5f' }
        },
        x: {
          ticks: { color: '#e0e6ed' },
          grid: { color: '#324a5f' }
        }
      }
    }
  });
});


