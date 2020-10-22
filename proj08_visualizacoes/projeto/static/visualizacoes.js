document.addEventListener('DOMContentLoaded', function () {
  var leitura_temp = [];
  var leitura_umidade = [];

  $.get("/api/v1.1/sensor/1/temp", function( data ) {
    resource = data.resource.slice(0, 10);
    resource.forEach(element => leitura_temp.push(
      parseFloat(parseFloat(element.valor).toFixed(2)))
    );
  });

  $.get("/api/v1.1/sensor/1/umidade", function( data ) {
    resource = data.resource.slice(0, 10);
    resource.forEach(element => leitura_umidade.push(
      parseFloat(parseFloat(element.valor).toFixed(2)))
    );

  }).done(function () {
    console.log(leitura_temp)
    console.log(leitura_umidade)
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
        data: leitura_temp
      }, {
        name: 'Umidade',
        data: leitura_umidade
      }]
    });
  });
});
