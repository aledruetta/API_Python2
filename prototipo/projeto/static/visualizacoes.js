/**
 * file: visualizacoes.js
 * library: highcharts.js
 *
 * Esse arquivo apresenta em tempo real e em formato de curva as leituras
 * recebidas pela API dos sensores. Um menu de seleção permite mudar a
 * origem dos dados segundo: local, sensor, parâmetro.
 */

$(function () {

  const URL_BASE = "/api/v1.1";
  const TIME_UPDATE = 10000;    // milliseconds

  /**
   * Retorna uma lista de objetos JSON com as infomações das estações cadastradas.
   */
  async function requestEstacoes() {
    const result = await fetch(`${URL_BASE}/estacao`);

    if (result.ok) {
      const data = await result.json();
      return data.resources;
    }
  }

  /**
   * Retorna uma lista de objetos JSON com as infomações dos sensores
   * da estação selecionada.
   */
  async function requestSensores(estacao_id) {
    const result = await fetch(`${URL_BASE}/estacao/${estacao_id}/sensor`);

    if (result.ok) {
      const data = await result.json();
      return data.resources;
    }
  }

  /**
   * Retorna uma lista de strings representando os parâmetros de leitura do sensor
   * selecionado.
   */
  async function requestParams(estacao_id, sensor_id) {
    const result = await fetch(`${URL_BASE}/estacao/${estacao_id}/sensor/${sensor_id}`);

    if (result.ok) {
      const data = await result.json();
      return data.resource.params.split(",");
    }
  }

  /**
   * Retorna uma lista de objetos JSON com as últimas 20 leituras efetuadas
   * pelo sensor para o parâmetro de leitura selecionado.
   */
  async function requestLeituras(sensor_id, param) {
    const result = await fetch(`${URL_BASE}/sensor/${sensor_id}/${param}/20`);

    if (result.ok) {
      const data = await result.json();
      return data.resources;
    }
  }

  /**
   * Chama as funções assíncronas e retorna um objeto JSON com as listas de
   * estações, sensores da primeira estação e parâmetros do primeiro sensor
   * da primeira estação.
   * Essas listas serão usadas para popular os menus de seleção drop-down e
   * para o gráfico inicial.
   */
  async function requestData() {
    const estacoes = await requestEstacoes();
    const sensores = await requestSensores(estacoes[0].id);
    const params = await requestParams(estacoes[0].id, sensores[0].id);

    return {estacoes, sensores, params};
  }

  function updateChart(serie, sensor_id, param) {

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

  }

  /**
   * Inicializa os dados dos menus de seleção drop-down.
   */
  function updateSelects(estacoes, sensores, params) {

    if (estacoes) {
      $('#local-sel').empty();
      estacoes.forEach(function(estacao) {
        $('#local-sel')
          .append($('<option></option>')
            .val(estacao.id)
            .text(`${estacao.local}#${estacao.id}`)
          );
      });
    }

    if (sensores) {
      $('#sensor-sel').empty();
      sensores.forEach(function(sensor) {
        $('#sensor-sel')
        .append($('<option></option>')
          .val(sensor.id)
          .text(`${sensor.tipo}#${sensor.id}`)
        );
      });
    }

    if (params) {
      $('#param-sel').empty();
      params.forEach(function(param) {
        $('#param-sel')
        .append($('<option></option>')
          .val(param)
          .text(`${param}`)
        );
      });
    }

  }

  requestData()
    /**
     * Inicializa o objeto Highcharts com os dados assícronos fornecidos
     * por requestData.
     */
    .then(function(data) {
      updateSelects(data.estacoes, data.sensores, data.params);

      let chart = new Highcharts.chart('container', {
        chart: {
          type: 'areaspline',
          animation: Highcharts.svg, // don't animate in old IE
          marginRight: 10,
          events: {
            load: function () {
              let estacoes = data.estacoes;
              let sensores = data.sensores;
              let params = data.params;

              let estacao_id = estacoes[0].id;
              let sensor_id = sensores[0].id;
              let param = params[0];

              const serie = this.series[0];
              serie.update({
                name: param,
              });

              $('#param-sel').change(function() {
                param = this.value;
                serie.update({
                  name: param
                });
              });

              $('#sensor-sel').change(function() {
                sensor_id = this.value;
                requestParams(estacao_id, sensor_id)
                  .then(function(params_new) {

                    params = params_new;
                    param = params[0]
                    serie.update({
                      name: param
                    });

                    updateSelects(null, null, params);
                  });
              });

              $('#local-sel').change(function() {
                estacao_id = this.value;
                requestSensores(estacao_id)
                  .then(function(sensores_new) {

                    sensores = sensores_new;
                    sensor = sensores[0]
                    params = sensor.params.split(",");
                    param = params[0]
                    serie.update({
                      name: param
                    });

                    updateSelects(null, sensores, params);
                  });
              });

              // set up the updating of the chart each second
              setInterval(function () {
                updateChart(serie, sensor_id, param);
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
          // data: chartInitialData,
          data: (function () {
            // generate an array of random data
            var data = [],
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

    });

}); // end load document
