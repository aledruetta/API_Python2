$(function () {

  let url_base = "/api/v1.1/";

  // preenche a lista de seleção das estações
  fetch(url_base + "estacao")

    .then(function(response) {
      var contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {
        return response.json()
        .then(function(json) {
          $('#origens').empty();
          json.resources.forEach(function(estacao) {
            $('#origens')
              .append($('<option></option>')
                .val(estacao.id)
                .text(estacao.local + ' #' + estacao.id)
              );
          });
        });
      }
    });

  $('#origens').change(function() {
    fetch(url_base + "estacao/" + this.value)
      .then(function(response) {
        var contentType = response.headers.get('content-type');
        if (contentType && contentType.indexOf("application/json") !== -1) {
          return response.json()
          .then(function(json) {
            alert(json.resource.id);
          });
        }
      });
  });

  Highcharts.chart('container', {
    chart: {
      type: 'area',
      animation: Highcharts.svg, // don't animate in old IE
      marginRight: 10,
      events: {
        load: function () {

          var umidade = this.series[0];
          var temperatura = this.series[1];

          // set up the updating of the chart each second
          setInterval(function () {
            ["umidade", "temperatura"].forEach(function(param) {

              fetch(url_base + "sensor/1/" + param + "/last")
                .then(function(response) {
                  var contentType = response.headers.get('content-type');

                  if (contentType && contentType.indexOf("application/json") !== -1) {
                    return response.json()

                    .then(function(json) {
                      // seconds (python) to milliseconds (js)
                      var x = json.resource.datahora * 1000;
                      var y = parseFloat(json.resource.valor);

                      if (param === "temperatura")
                        temperatura.addPoint([x, y], true, true);
                      else if (param === "umidade")
                        umidade.addPoint([x, y], true, true);
                    });
                  }
                });

            });
          }, 1000);
        }
      }
    },

    time: {
        useUTC: false
    },

    title: {
        text: 'Live random data'
    },

    accessibility: {
        announceNewData: {
            enabled: true,
            minAnnounceInterval: 15000,
            announcementFormatter: function (allSeries, newSeries, newPoint) {
                if (newPoint) {
                    return 'New point added. Value: ' + newPoint.y;
                }
                return false;
            }
        }
    },

    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },

    yAxis: {
        title: {
            text: 'Value'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },

    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x:%Y-%m-%d %H:%M:%S}<br/>{point.y:.2f}'
    },

    legend: {
        enabled: true
    },

    exporting: {
        enabled: false
    },

    series: [
      {
        name: 'Umidade',
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -299; i <= 0; i += 1) {
                let x = time + i * 1000;
                let y = 0;
                data.push({
                    x: time + i * 1000,
                    y: 0
                });
            }
            return data;
        }())
      },
      {
        name: 'Temperatura',
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -299; i <= 0; i += 1) {
                let x = time + i * 1000;
                let y = 0;
                data.push({
                    x: time + i * 1000,
                    y: 0
                });
            }
            return data;
        }())
      },
    ]
  });
});
