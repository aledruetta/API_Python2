document.addEventListener('DOMContentLoaded', function () {
  var myChart = Highcharts.chart('container', {
    chart: {
      type: 'area'
    },
    title: {
      text: 'Média Anual'
    },
    xAxis: {
      categories: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    },
    yAxis: {
      title: {
        text: 'Leitura'
      }
    },
    series: [{
      name: 'Temperatura',
      data: [23, 41, 8, 12, 18, 22, 19.04, 39, 33.2, 11, 0, -4.7]
    }, {
      name: 'Umidade',
      data: [33, 32, 8, 76, 70, 22, 19.04, 68, 15.2, 7, 12, 97]
    }]
  });
});
