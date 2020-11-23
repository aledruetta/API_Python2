$(function () {

  const URL_BASE = "/api/v1.1";
  const TIME_UPDATE = 10000;    // milliseconds

  fetch(`${URL_BASE}/estacao`)

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

          return fetch(`${URL_BASE}/estacao/${estacao.id}/sensor`);
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

          return fetch(`${URL_BASE}/estacao/${sensor.estacao_id}/sensor/${sensor.id}`);
        });
      }
    }) // end fetch sensores

    .then(function getParams(response) {
      let contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {

        return response.json()
        .then(function(json) {

          $('#param-sel').empty();

          let params = json.resource.params.split(",");
          params.forEach(function(param) {
            $('#param-sel')
            .append($('<option></option>')
              .val(param)
              .text(`${param}`)
            );
          });

          let param = params[0];
          let sensor_id = json.resource.id;

          return fetch(`${URL_BASE}/sensor/${sensor_id}/${param}/20`);
        });
      }
    })  // end fetch params

    .then(function getLeituras(response) {
      let contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {

        return response.json()
        .then(function(json) {

          return {
            param: json.resources[0].param,
            sensor_id: json.resources[0].sensor_id,
            leituras: json.resources
          };

        });
      }
    }) // end fetch leituras

    .then(function setCharts(json) {

      let data = [];

      for (let i = 0; i < 20; i += 1) {
        data.push({
          x: json.leituras[i].datahora,
          y: json.leituras[i].valor
        });
      }

      const chart = createHighchart(json.param, json.sensor_id);
    });


  function createHighchart (param, sensor_id) {
    return Highcharts.chart('container', {
      chart: {

        type: 'areaspline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {

          load: function () {
            this.update({
              series: {
                name: param,
              }
            });
            const series = this.series[0];

            // set up the updating of the chart each second
            setInterval(function () {

              $('#param-sel').change(function() {
                param = this.value;
                series.update({
                  name: param
                });
              });

              fetch(`${URL_BASE}/sensor/${sensor_id}/${param}/1`)
              .then(function(response) {
                let contentType = response.headers.get('content-type');
                if (contentType && contentType.indexOf("application/json") !== -1) {

                  return response.json()
                  .then(function(json) {
                    // seconds (python) to milliseconds (js)
                    let x = json.resources[0].datahora * 1000;
                    let y = parseFloat(json.resources[0].valor);

                    console.log(param, x, y);
                    series.addPoint([x, y], true, true);
                  });
                }
              });
            }, TIME_UPDATE);

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

          for (i = -19; i <= 0; i += 1) {
              data.push({
                  x: time + i * TIME_UPDATE,
                  y: 0
              });
          }
          return data;
        }()),
        fillColor: {
          linearGradient: {
              x1: 0,
              y1: 0,
              x2: 0,
              y2: 1
          },
          stops: [
              [0, Highcharts.getOptions().colors[0]],
              [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
          ]
        }
      }]

    });
  }

}); // end load document
