$(function () {

  const url_base = "/api/v1.1";

  fetch(`${url_base}/estacao`)

    .then(function getEstacoes(response) {
      let contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {

        return response.json()
        .then(function(json) {
          $('#local-sel').empty();

          let estacoes = json.resources;
          estacoes.forEach(function(estacao) {
            $('#local-sel')
              .append($('<option></option>')
                .val(estacao.id)
                .text(`${estacao.local}#${estacao.id}`)
              );
          });

          let estacao = estacoes[0];

          return fetch(`${url_base}/estacao/${estacao.id}/sensor`);
        });
      }
    }) // end fetch estacoes

    .then(function getSensores(response) {
      let contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {

        return response.json()
        .then(function(json) {
          $('#sensor-sel').empty();

          let sensores = json.resources;
          sensores.forEach(function(sensor) {
            $('#sensor-sel')
            .append($('<option></option>')
              .val(sensor.id)
              .text(`${sensor.tipo}#${sensor.id}`)
            );
          });

          let sensor = sensores[0];

          return fetch(`${url_base}/estacao/${sensor.estacao_id}/sensor/${sensor.id}`);
        });
      }
    }) // end fetch sensores

    .then(function getParams(response) {
      let contentType = response.headers.get('content-type');
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
            tipo: 'areaspline',
            param: params[0],
            sensor_id: json.resource.id
          };

        });
      }
    }) // end fetch params

    .then(function(json) {
      const chart = createHighchart(json.tipo, json.param, json.sensor_id);
      chart.update({
        series: { name: json.param }
      });
    });


  function createHighchart (tipo, param, sensor_id) {
    return Highcharts.chart('container', {
      chart: {
        type: tipo,
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
          load: function () {

            let serie = this.series[0];

            // set up the updating of the chart each second
            setInterval(function () {

              $('#param-sel').change(function() {
                param = this.value;
                serie.update({
                  name: param
                });
              });

              fetch(`${url_base}/sensor/${sensor_id}/${param}/last`)
              .then(function(response) {
                let contentType = response.headers.get('content-type');
                if (contentType && contentType.indexOf("application/json") !== -1) {

                  return response.json()
                  .then(function(json) {
                    // seconds (python) to milliseconds (js)
                    let x = json.resource.datahora * 1000;
                    let y = parseFloat(json.resource.valor);

                    console.log(param, x, y);
                    serie.addPoint([x, y], true, true);
                  });
                }
              });
            }, 10000);

          }
        }
      },

      time: {
          useUTC: false
      },

      title: {
          text: null
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
        name: null,
        data: (function () {
          // generate an array of random data
          let data = [],
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
