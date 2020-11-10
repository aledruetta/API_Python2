$(function () {

  /*

    fetch estacoes
      then
        return response
      then
        vaciar listas
        popular lista estacoes
        return fetch sensores
      then
        return response
      then
        popular lista sensores
        return fetch params
      then
        return response
      then
        popular lista params
        criar highchart

   */

  var url_base = "/api/v1.1";

  fetch(`${url_base}/estacao`)

    .then(function(response) {
      var contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {

        return response.json()
        .then(function(json) {
          $('#local-sel').empty();

          var estacoes = json.resources;
          estacoes.forEach(function(estacao) {
            $('#local-sel')
              .append($('<option></option>')
                .val(estacao.id)
                .text(`${estacao.local}#${estacao.id}`)
              );
          });

          var estacao = estacoes[0];

          return fetch(`${url_base}/estacao/${estacao.id}/sensor`);
        });
      }
    }) // end fetch estacoes

    .then(function(response) {
      var contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {

        return response.json()
        .then(function(json) {
          $('#sensor-sel').empty();

          var sensores = json.resources;
          sensores.forEach(function(sensor) {
            $('#sensor-sel')
            .append($('<option></option>')
              .val(sensor.id)
              .text(`${sensor.tipo}#${sensor.id}`)
            );
          });

          var sensor = sensores[0];

          return fetch(`${url_base}/estacao/${sensor.estacao_id}/sensor/${sensor.id}`);
        });
      }
    }) // end fetch sensores

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

          return {
            param: params[0],
            sensor_id: json.resource.id
          };

        });
      }
    }) // end fetch params

    .then(function(json) {
      var chart = createHighchart('area', json.param, json.sensor_id);
    });

  function createHighchart (type, param, sensor_id) {
    return Highcharts.chart('container', {
      chart: {
        type: type,
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
          load: function () {

            var serie = this.series[0];

            // set up the updating of the chart each second
            setInterval(function () {

              fetch(`${url_base}/sensor/${sensor_id}/${param}/last`)
              .then(function(response) {
                var contentType = response.headers.get('content-type');
                if (contentType && contentType.indexOf("application/json") !== -1) {

                  return response.json()
                  .then(function(json) {
                    // seconds (python) to milliseconds (js)
                    var x = json.resource.datahora * 1000;
                    var y = parseFloat(json.resource.valor);

                      console.log(param, x, y);
                      serie.addPoint([x, y], true, true);
                    });
                }
              });
            }, 5000);

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

      series: [{
        name: 'Random data',
        data: (function () {
          // generate an array of random data
          var data = [],
            time = (new Date()).getTime(),
            i;

          for (i = -18; i <= 0; i += 1) {
            data.push({
              x: time + i * 5000,
              y: null
            });
          }
          return data;
        }())
      }]

    });
  }

}); // end load document

  /*
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

                        for (i = -50; i <= 0; i += 1) {
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
  */
