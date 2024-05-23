const showChartBtn = document.getElementById('show-chart-btn');
const hideChartBtn = document.getElementById('hide-chart-btn');
const chartContainer = document.getElementById('parameter-chart-container');
const parameterSelect = document.getElementById('parameter-select');
const startDatePicker = document.getElementById('start-date');
const endDatePicker = document.getElementById('end-date');


showChartBtn.addEventListener('click', function () {
    const currentParameter = parameterSelect.value;
    const startDate = startDatePicker.value;
    const endDate = endDatePicker.value;
    const graph_url_param = `${graph_url}?parameter=${currentParameter}&start_date=${startDate}&end_date=${endDate}`;

    fetch(graph_url_param)
        .then(response => response.json())
        .then(data => {
            if (chartContainer.style.display === 'none') {
                chartContainer.style.display = 'block';
            }

            Highcharts.chart('chart-content', {
                title: {
                    text: `${currentParameter.charAt(0).toUpperCase() + currentParameter.slice(1)} Levels Over Time`
                },
                xAxis: {
                    title: {
                        text: 'Date'
                    },
                    categories: data.change_dates
                },
                yAxis: {
                    title: {
                        text: currentParameter.charAt(0).toUpperCase() + currentParameter.slice(1)
                    }
                },
                series: [{
                    name: currentParameter.charAt(0).toUpperCase() + currentParameter.slice(1),
                    data: data.parameter_values
                }]
            });
        });
});

hideChartBtn.addEventListener('click', function () {
    chartContainer.style.display = 'none';
});