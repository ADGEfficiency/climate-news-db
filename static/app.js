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

// this requests the file and executes a callback with the parsed result once
//   it is available
fetchJSONFile('/years.json', (data) => {
  const years = Array.from(data.years);
  delete data.years;

  // now need to create a list of objects
  const datasets = [];

  for (const [key, value] of Object.entries(data)) {
    console.log(`${key}: ${value}`);
    const ds = {};
    ds.label = key;
    ds.backgroundColor = 'red';
    ds.data = value;

    datasets.push(ds);
  }
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
        mode: 'index',
        intersect: false,
      },
      legend: {
        position: 'bottom',
      },
      scales: {
        xAxes: [{
          stacked: true,
        }],
        yAxes: [{
          stacked: true,
        }],
      },
    },
  });
});
