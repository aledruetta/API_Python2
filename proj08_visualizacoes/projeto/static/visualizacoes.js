document.addEventListener('DOMContentLoaded', function () {
  var myChart = Highcharts.chart('container', {
    chart: {
      type: 'spline',
      animation: Highcharts.svg, // don't animate in old IE
      marginRight: 10,
      events: {
        load: function () {
          var temperatura = this.series[0];
          setInterval(function () {
            fetch("/api/v1.1/sensor/1/temp/last")
            .then(function(response) {
              var contentType = response.headers.get('content-type');
              if (contentType && contentType.indexOf("application/json") !== -1) {
                return response.json()
                .then(function(json) {
                  var x = json.resource.datahora;
                  var y = parseFloat(json.resource.valor);
                  temperatura.addPoint([x, y], true, true);
                  console.log(temperatura.data);
                });
              }
            });
          }, 1000);
        }
      }
    },
    time: {
      useUTC: false
    },
    title: {
      text: 'Média Anual'
    },
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150
    },
    yAxis: {
      title: {
        text: 'Leitura'
      }
    },
    series: [{
      name: 'Temperatura',
      data: (function () {
        var data = [],
            time = (new Date()).getTime(),
            i;

        for (i = -9; i <= 0; i += 1) {
            data.push({
              x: time + i * 1000,
              y: null
            });
        }
        return data;
      }())
    }]
  });
});
