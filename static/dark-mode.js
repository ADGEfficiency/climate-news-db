
/** doc */
function updateChartColors(theme) {
  const chart = window.myBar;

  if (theme === 'dark') {
    chart.data.datasets.forEach((dataset, i) => {
      // dataset.backgroundColor = `rgba(255, 255, 255, 0.${i + 5})`;
      dataset.borderColor = `rgba(255, 255, 255, 0.0)`;
      // dataset.hoverBackgroundColor = `rgba(255, 255, 255, 0.${i + 8})`;
    });
    const colo = 'rgba(255, 255, 255, 0.8)'
    chart.options.scales.xAxes[0].gridLines.color = 'rgba(255, 255, 255, 0.4)';
    chart.options.scales.yAxes[0].gridLines.color = 'rgba(255, 255, 255, 0.4)';
    // chart.options.legend.labels.fontColor = colo;
    // chart.options.scales.xAxes[0].ticks.fontColor = colo;
    // chart.options.scales.yAxes[0].ticks.fontColor = colo;
    // chart.options.scales.yAxes[0].scaleLabel.fontColor = colo;

  } else {
    chart.data.datasets.forEach((dataset, i) => {
      // dataset.backgroundColor = `rgba(54, 162, 235, 0.${i + 5})`;
      dataset.borderColor = `rgba(54, 162, 235, 0.0)`;
      // dataset.hoverBackgroundColor = `rgba(54, 162, 235, 0.${i + 8})`;
    });
    chart.options.scales.xAxes[0].gridLines.color = 'rgba(0, 0, 0, 0.1)';
    chart.options.scales.yAxes[0].gridLines.color = 'rgba(0, 0, 0, 0.1)';

    chart.options.scales.yAxes[0].scaleLabel.fontColor = '#666666';
    // chart.options.legend.labels.fontColor = 'black';
    // chart.options.scales.xAxes[0].ticks.fontColor = 'black';

    // chart.options.scales.yAxes[0].ticks.fontColor = 'black';
    // chart.options.scales.yAxes[0].scaleLabel.fontColor = 'black';
    // chart.options.scales.yAxes[0].ticks.fontColor = 'black';
  }

  chart.update();
}

/** doc */
function toggleDarkMode() {
  const html = document.documentElement;
  const icon = document.getElementById('darkModeToggle');

  if (html.classList.contains('dark')) {
    html.classList.remove('dark');
    localStorage.theme = 'light';
    icon.classList.replace('bi-moon', 'bi-brightness-high');
    icon.classList.remove('white-icon');
    updateChartColors('light');
  } else {
    html.classList.add('dark');
    localStorage.theme = 'dark';
    icon.classList.replace('bi-brightness-high', 'bi-moon');
    icon.classList.add('white-icon');
    updateChartColors('dark');
  }
}
