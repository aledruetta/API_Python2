document.addEventListener('DOMContentLoaded', function () {
  Highcharts.chart('container', {
      chart: {
          type: 'spline',
          animation: Highcharts.svg, // don't animate in old IE
          marginRight: 10,
          events: {
              load: function () {

                  // set up the updating of the chart each second
                  var series = this.series[0];
                  setInterval(function () {
                      var x = (new Date()).getTime(), // current time
                          y = Math.random();
                      series.addPoint([x, y], true, true);
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
          enabled: false
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

              for (i = -19; i <= 0; i += 1) {
                  data.push({
                      x: time + i * 1000,
                      y: Math.random()
                  });
              }
              return data;
          }())
      }]
  });
});

// document.addEventListener('DOMContentLoaded', function () {
//   var myChart = Highcharts.chart('container', {
//     chart: {
//       type: 'spline',
//       animation: Highcharts.svg, // don't animate in old IE
//       marginRight: 10,
//       events: {
//         load: function () {
//           var temperatura = this.series[0];
//           setInterval(function () {
//             fetch("/api/v1.1/sensor/1/temp/last")
//             .then(function(response) {
//               var contentType = response.headers.get('content-type');
//               if (contentType && contentType.indexOf("application/json") !== -1) {
//                 return response.json()
//                 .then(function(json) {
//                   var x = json.resource.datahora;
//                   var y = parseFloat(json.resource.valor);
//                   temperatura.addPoint([x, y], true, true);
//                   console.log(temperatura.data);
//                 });
//               }
//             });
//           }, 1000);
//         }
//       }
//     },
//     time: {
//       useUTC: false
//     },
//     title: {
//       text: 'Média Anual'
//     },
//     xAxis: {
//       type: 'datetime',
//       tickPixelInterval: 150
//     },
//     yAxis: {
//       title: {
//         text: 'Leitura'
//       }
//     },
//     series: [{
//       name: 'Temperatura',
//       data: (function () {
//         var data = [],
//             time = (new Date()).getTime(),
//             i;
//
//         for (i = -9; i <= 0; i += 1) {
//             data.push({
//               x: time + i * 1000,
//               y: null
//             });
//         }
//         return data;
//       }())
//     }]
//   });
// });
