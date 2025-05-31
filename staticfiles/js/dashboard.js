document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('productCnt').innerText = backendData.product_cnt;
  document.getElementById('stockCnt').innerText = backendData.stock;
  document.getElementById('totalSales').innerText = backendData.year_total_sales.toLocaleString();

  // Yil select
  const yearSelect = document.getElementById('yearSelect');
  const thisYear = new Date().getFullYear();
  for (let y = thisYear - 4; y <= thisYear; y++) {
    const opt = document.createElement('option');
    opt.value = y;
    opt.text = y;
    if (y == backendData.year) opt.selected = true;
    yearSelect.appendChild(opt);
  }

  // Pie chart
  new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
      labels: backendData.pie_labels,
      datasets: [{
        data: backendData.pie_data,
        backgroundColor: [
          "#2684ff", "#00d084", "#fcbb13", "#e74c3c", "#6c5ce7", "#00b894", "#fdcb6e", "#d63031"
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });

  // Bar+Line (combined) chart
  new Chart(document.getElementById('barLineChart'), {
    type: 'bar',
    data: {
      labels: backendData.months,
      datasets: [
        {
          label: 'Revenue',
          data: backendData.bar_rev,
          backgroundColor: "#2684ff",
          yAxisID: 'y'
        },
        {
          label: 'Cost',
          data: backendData.bar_cost,
          backgroundColor: "#fcbb13",
          yAxisID: 'y'
        },
        {
          label: 'Profit',
          data: backendData.line_profit,
          type: 'line',
          borderColor: "#00d084",
          backgroundColor: "#00d08422",
          fill: false,
          tension: 0.2,
          yAxisID: 'y'
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { position: 'top' } },
      scales: { y: { beginAtZero: true } }
    }
  });
});