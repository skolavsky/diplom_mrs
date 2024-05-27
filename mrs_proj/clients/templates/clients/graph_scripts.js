const showChartBtn = document.getElementById('show-chart-btn');
const hideChartBtn = document.getElementById('hide-chart-btn');
const chartContainer = document.getElementById('parameter-chart-container');
const parameterSelect = document.getElementById('parameter-select');
const startDatePicker = document.getElementById('start-date');
const endDatePicker = document.getElementById('end-date');
const showNormValuesCheckbox = document.getElementById('show-norm-values');

showChartBtn.addEventListener('click', function () {
    const currentParameter = parameterSelect.value;
    const startDate = startDatePicker.value;
    const endDate = endDatePicker.value;
    const showNormValues = showNormValuesCheckbox.checked ? '1' : '0';
    const graph_url_param = `${graph_url}?parameter=${currentParameter}&start_date=${startDate}&end_date=${endDate}&show_norm_values=${showNormValues}`;

    fetch(graph_url_param)
        .then(response => response.json())
        .then(data => {
            if (chartContainer.style.display === 'none') {
                chartContainer.style.display = 'block';
            }

            const seriesData = [{
                name: currentParameter.charAt(0).toUpperCase() + currentParameter.slice(1),
                data: data.parameter_values
            }];

            if (showNormValuesCheckbox.checked) {
                seriesData.push(
                    {
                        name: 'Верхний порог нормы',
                        data: data.upper_limit,
                        dashStyle: 'ShortDash',
                        color: 'red'
                    },
                    {
                        name: 'Нижний порог нормы',
                        data: data.lower_limit,
                        dashStyle: 'ShortDash',
                        color: 'blue'
                    }
                );
            }

            Highcharts.chart('chart-content', {
                title: {
                    text: `${currentParameter.charAt(0).toUpperCase() + currentParameter.slice(1)} Уровень`
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
                series: seriesData
            });
        });
});

hideChartBtn.addEventListener('click', function () {
    chartContainer.style.display = 'none';
});
