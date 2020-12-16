/**
 * file: visualizacoes.js
 * library: highcharts.js
 *
 * Esse arquivo apresenta em tempo real e em formato de curva as leituras
 * recebidas pela API dos sensores. Um menu de seleção permite mudar a
 * origem dos dados segundo: local, sensor, parâmetro.
 */

$(function () {

  const versao = "v1.2"
  const URL_BASE = `/api/${versao}`;
  const TIME_UPDATE = 10000;    // milliseconds

  /**
   * Retorna uma lista de objetos JSON com as infomações das estações cadastradas.
   */
  async function requestEstacoes() {
    const result = await fetch(`${URL_BASE}/estacao`);

    if (result.ok) {
      let data = await result.json();
      return data.resources.sort((a, b) => {return a.id > b.id});
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
      return data.resources.sort((a, b) => {return a.id > b.id});
    }
  }

  /**
   * Retorna uma lista de strings representando os parâmetros de leitura do sensor
   * selecionado.
   */
  async function requestParams(estacao_id, sensor_id) {
    const result = await fetch(`${URL_BASE}/sensor/${sensor_id}`);

    if (result.ok) {
      const data = await result.json();
      return data.resource.params.split(",").sort();
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
    .then((response) => {
      let contentType = response.headers.get('content-type');
      if (contentType && contentType.indexOf("application/json") !== -1) {

        return response.json()
        .then((json) => {
          // seconds (python) to milliseconds (js)
          let x = json.resources[0].datahora * 1000;
          let y = parseFloat(json.resources[0].valor);

          console.log(`#${sensor_id} ${param} [${x}, ${y}]`);
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
      estacoes.forEach((estacao) => {
        $('#local-sel')
          .append($('<option></option>')
            .val(estacao.id)
            .text(`${estacao.local}#${estacao.id}`)
          );
      });
    }

    if (sensores) {
      $('#sensor-sel').empty();
      sensores.forEach((sensor) => {
        $('#sensor-sel')
        .append($('<option></option>')
          .val(sensor.id)
          .text(`${sensor.tipo}#${sensor.id}`)
        );
      });
    }

    if (params) {
      $('#param-sel').empty();
      params.forEach((param) => {
        $('#param-sel')
        .append($('<option></option>')
          .val(param)
          .text(param)
        );
      });
    }

  }

  requestData()
    /**
     * Inicializa o objeto Highcharts com os dados assícronos fornecidos
     * por requestData.
     */
    .then((data) => {

      let chart = new Highcharts.chart('container', {
        chart: {
          type: 'areaspline',
          animation: Highcharts.svg, // don't animate in old IE
          marginRight: 10,
          events: {
            load: function() {

              const selected = {
                estacao_id: data.estacoes[0].id,
                sensor_id: data.sensores[0].id,
                param: data.params[0],
              };

              const serie = this.series[0];

              updateSelects(data.estacoes, data.sensores, data.params);

              serie.update({
                name: selected.param
              });

              $('#param-sel').change(function() {
                selected.param = this.value;

                serie.update({
                  name: selected.param
                });
              });

              $('#sensor-sel').change(function() {
                selected.sensor_id = this.value;

                requestParams(selected.estacao_id, selected.sensor_id)
                  .then((params_new) => {

                    data.params = params_new;
                    selected.param = data.params[0];

                    serie.update({
                      name: selected.param
                    });

                    updateSelects(null, null, data.params);
                  });
              });

              $('#local-sel').change(function() {
                selected.estacao_id = this.value;

                requestSensores(selected.estacao_id)
                  .then((sensores_new) => {

                    data.sensores = sensores_new;
                    selected.sensor_id = data.sensores[0].id;
                    data.params = data.sensores[0].params.split(",");
                    selected.param = data.params[0]

                    serie.update({
                      name: selected.param
                    });

                    updateSelects(null, data.sensores, data.params);
                  });
              });

              // set up the updating of the chart each second
              setInterval(() => {
                if (serie && selected.sensor_id && selected.param) {
                  updateChart(serie, selected.sensor_id, selected.param);
                }
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
            announcementFormatter: (allSeries, newSeries, newPoint) => {
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
