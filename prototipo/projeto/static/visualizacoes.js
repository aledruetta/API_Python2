$(function () {

  const URL_BASE = "/api/v1.1";
  const TIME_UPDATE = 10000;    // milliseconds

  async function requestEstacoes() {
    const result = await fetch(`${URL_BASE}/estacao`);

    if (result.ok) {
      const data = await result.json();

      $('#local-sel').empty();

      let estacoes = data.resources;
      estacoes.forEach(function(estacao) {
        $('#local-sel')
          .append($('<option></option>')
            .val(estacao.id)
            .text(`${estacao.local}#${estacao.id}`)
          );
      });

      return estacoes[0];
    }
  }

  async function requestSensores(estacao) {
    const result = await fetch(`${URL_BASE}/estacao/${estacao.id}/sensor`);

    if (result.ok) {
      const data = await result.json();

      $('#sensor-sel').empty();

      let sensores = data.resources;
      sensores.forEach(function(sensor) {
        $('#sensor-sel')
        .append($('<option></option>')
          .val(sensor.id)
          .text(`${sensor.tipo}#${sensor.id}`)
        );
      });

      return sensores[0];
    }
  }

  async function requestParams(estacao, sensor) {
    const result = await fetch(`${URL_BASE}/estacao/${estacao.id}/sensor/${sensor.id}`);

    if (result.ok) {
      const data = await result.json();

      $('#param-sel').empty();

      let params = data.resource.params.split(",");
      params.forEach(function(param) {
        $('#param-sel')
        .append($('<option></option>')
          .val(param)
          .text(`${param}`)
        );
      });

      return params[0];
    }
  }

  async function requestLeituras(sensor, param) {
    const result = await fetch(`${URL_BASE}/sensor/${sensor.id}/${param}/20`);

    if (result.ok) {
      const data = await result.json();

      return data.resources;
    }
  }

  async function requestData() {
    const estacao = await requestEstacoes();
    const sensor = await requestSensores(estacao);
    const param = await requestParams(estacao, sensor);
    return await requestLeituras(sensor, param);
  }

  let chart = new Highcharts.chart('container', {
    chart: {
      type: 'areaspline',
      animation: Highcharts.svg, // don't animate in old IE
      marginRight: 10,
      events: {
        load: function () {
          const self = this;

          requestData()
            .then(function(leituras) {

              let param = leituras[0].param;
              let sensor_id = leituras[0].sensor_id;

              let chartData = [];
              let time = (new Date()).getTime() * 1000;

              for (let i=0; i<20; i++) {
                let leitura = leituras[19-i];
                chartData.push({
                  x: time - i * TIME_UPDATE,
                  y: leitura.valor
                });
              }

              const serie = self.series[0];
              // serie.setData(chartData);

              serie.update({
                name: param
              });

              // set up the updating of the chart each second
              setInterval(function () {

                $('#param-sel').change(function() {
                  param = this.value;
                  serie.update({
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
                      serie.addPoint([x, y], true, true);
                    });
                  }
                });
              }, TIME_UPDATE);

            });
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
      data: [{}],
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

}); // end load document
