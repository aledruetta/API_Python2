$(function () {

  let url_base = "/api/v1.1";

  // preenche os campos de seleção
  fetch(`${url_base}/estacao`)
  .then(function(response) {
    var contentType = response.headers.get('content-type');
    if (contentType && contentType.indexOf("application/json") !== -1) {

      return response.json()
      .then(function(json) {
        $('#local-sel').empty();

        estacoes = json.resources;
        estacoes.forEach(function(estacao) {
          $('#local-sel')
            .append($('<option></option>')
              .val(estacao.id)
              .text(`${estacao.local}#${estacao.id}`)
            );
        });

        fetch(`${url_base}/estacao/${estacoes[0].id}/sensor`)
        .then(function(response) {
          var contentType = response.headers.get('content-type');
          if (contentType && contentType.indexOf("application/json") !== -1) {

            return response.json()
            .then(function(json) {
              $('#sensor-sel').empty();

              sensores = json.resources;
              sensores.forEach(function(sensor) {
                $('#sensor-sel')
                .append($('<option></option>')
                  .val(sensor.id)
                  .text(`${sensor.tipo}#${sensor.id}`)
                );
              });

              fetch(`${url_base}/estacao/${estacoes[0].id}/sensor/${sensores[0].id}`)
              .then(function(response) {
                var contentType = response.headers.get('content-type');
                if (contentType && contentType.indexOf("application/json") !== -1) {

                  return response.json()
                  .then(function(json) {
                    $('#param-sel').empty();

                    params = json.resource.params.split(",");
                    params.forEach(function(param) {
                      $('#param-sel')
                      .append($('<option></option>')
                        .val(param)
                        .text(`${param}`)
                      );
                    });
                  });
                }
              });
            });
          }
        });
      });
    }
  });

  // Observa mudanças na lista de seleção
  $('#origens').change(function() {
    //
    // Recupera a lista de sensores da estação selecionada
    fetch(`${url_base}/estacao/${this.value}/sensor`)
      .then(function(response) {
        var contentType = response.headers.get('content-type');
        if (contentType && contentType.indexOf("application/json") !== -1) {
          return response.json()

          // Atualiza o gráfico com a informação dos sensores
          .then(function(json) {
            sensores = json.resources;
            sensores.forEach(function (sensor) {
              sensor.params.split(",")
                .forEach(function (param) {
                  this.series.append({
                    name: param,
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
                  });
                });
            });

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
            sensores.forEach(function (sensor) {
              sensor.params.split(",")
                .forEach(function(param) {
                  fetch(`${url_base}/sensor/${sensor.id}/${param}/last`)
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

    series: []
  });

});
