
/** loads json from server */
function fetchJSONFile(path, callback) {
  const httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function () {
    if (httpRequest.readyState === 4) {
      if (httpRequest.status === 200) {
        const data = JSON.parse(httpRequest.responseText);
        if (callback) callback(data);
      }
    }
  };
  httpRequest.open('GET', path);
  httpRequest.send();
}

/** creates a chart */
function main() {
  fetchJSONFile('/newspaper-by-year.json', (data) => {
    const years = Array.from(data.years);
    const datasets = Array.from(data.datasets);

    console.log(datasets);
    const barChartData = {
      labels: years,
      datasets,
    };

    const ctx = document.getElementById('canvas').getContext('2d');
    window.myBar = new Chart(ctx, {
      type: 'bar',
      data: barChartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
          mode: 'nearest',
          intersect: true,
          yAlign: 'top'
        },
        legend: {
          display: false,
        },
        scales: {
          xAxes: [{
            stacked: true,
            gridLines: {
                  display: false,
                },
          }],
          yAxes: [{
            stacked: true,
            scaleLabel: {
              display: true,
              labelString: 'Articles',
              fontSize: 12,
            },
            gridLines: {
                  display: false,
                },
          }],
        },
    animation: {
        duration : 2000,
        easing : 'easeInOutQuint'
    },
      },
    });
  });
}

main()
