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

var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {};

xhr.open('GET', '/years.json');
xhr.send();

// this requests the file and executes a callback with the parsed result once
//   it is available
fetchJSONFile('/years.json', (data) => {

  years = Array.from(data.years);
  delete data.years;

  // now need to create a list of objects
  let datasets = []

  for (const [key, value] of Object.entries(data)) {
    console.log(`${key}: ${value}`);
    let ds = {}
    ds['label'] = key;
    ds['backgroundColor'] = 'red'
    ds['data'] = value

    datasets.push(ds);
  }
  console.log(datasets)

  const barChartData = {
    labels: years,
    datasets: datasets,
    // datasets: [{
    //   label: 'Dataset 1',
    //   backgroundColor: 'red',
    //   stack: 'Stack 0',
    //   data: data.nytimes,
    // }, {
    //   label: 'Dataset 2',
    //   backgroundColor: 'red',
    //   stack: 'Stack 0',
    //   data: data.nytimes,
    // }, {
    //   label: 'Dataset 3',
    //   backgroundColor: 'red',
    //   stack: 'Stack 1',
    //   data: data.nytimes,
    // }],
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
