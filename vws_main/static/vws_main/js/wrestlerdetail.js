new WOW().init();
$('[data-toggle="popover"]').popover();
$('.popover-dismiss').popover({
  trigger: 'focus'
});
$(document).ready(function () {
  $('#matchestable').DataTable({
    'info': false,
    'paging':false,
    'scrollY': '300px',
    'scrollCollapse': true,
    "order":[[1, "asc"]]
  });
  $('.dataTables_length').addClass('bs-select');
});
  //bar
var resulthist = document.getElementById("resultchart").getContext('2d');
var myBarChart = new Chart(resulthist, {
  type: 'bar',
  data: {
    labels: {{resulttypes | safe}},
    datasets: [{
      label: 'Result Type',
      data: {{resulttypecounts | safe}},
      backgroundColor: 'rgb(63, 81, 181, 0.8)',
    }]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          stepSize: 1.0
        }
      }]
    },
     title: {
        display: true,
        text: 'Result Distribution'
    },
     legend: {
        display: false},
    responsive: true,
    animation: {
      duration: 2000
    }
  }
});
  //line
var vsline = document.getElementById("vslinechart").getContext('2d');
var myLineChart = new Chart(vsline, {
  type: 'line',
  data: {
    labels: {{vsindex | safe}},
    datasets: [{
        label: "World Average",
        data: {{worldvs | safe}},
        borderColor: 'rgb(255, 235, 59)',
        backgroundColor: 'rgb(255, 255, 255, 0.0)',
        borderWidth: 2
      },
      {
        label: "Veritas Score",
        data: {{vsvalues | safe}},
        borderColor: 'rgb(63, 81, 181)',
        backgroundColor: 'rgb(63, 81, 181, 0.3)',
        borderWidth: 2
      },
    ]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          stepSize: 10.0
        }
      }]
    },
    title: {
        display: true,
        text: 'Veritas Score over Time'
    },
    responsive: true,
    animation: {
      'duration': 2000
    }
  }
});
    //radar
var focusradar = document.getElementById("focusshotchart").getContext('2d');
var myRadarChart = new Chart(focusradar, {
  type: 'radar',
  data: {
    labels: {{shot_labels | safe}},
    datasets: [
    {
        label: "Effeciency (% of converted)",
        data: {{rates | safe}},
        backgroundColor: 'rgb(63, 81, 181, 0.5)',
        borderColor: 'rgb(63, 81, 181)',
        borderWidth: 2,
        pointBackgroundColor: 'rgb(63, 81, 181)'
      },
    {
        label: "Preference (% of total)",
        data: {{prefs | safe}},
        backgroundColor: 'rgb(255, 235, 59, 0.5)',
        borderColor: 'rgb(255, 235, 59)',
        borderWidth: 2,
        pointBackgroundColor: 'rgb(255, 235, 59)'
      }
    ]
  },
  options: {
    scale: {ticks: {
            min:0,
            }
    },
    scales: {
        xAxes: [{
              display: false,
            gridLines: {
                display:false
            }
        }],
        yAxes: [{
          display: false,
            gridLines: {
                display:false
            }
        }]
    },
     title: {
        display: true,
        text: 'Focus Shot Distribution Chart'
    },
    responsive: true,
    animation: {duration:2000}
  }
});
        //radar
var oppradar = document.getElementById("oppshotchart").getContext('2d');
var myRadarChart = new Chart(oppradar, {
  type: 'radar',
  data: {
    labels: {{shot_labels | safe}},
    datasets: [
      {
        label: "Effeciency (% converted)",
        data: {{orates | safe}},
        backgroundColor: 'rgb(63, 81, 181, 0.5)',
        borderColor: 'rgb(63, 81, 181)',
        borderWidth: 2,
        pointBackgroundColor: 'rgb(63, 81, 181)'
      },
      {
        label: "Preference (% of total)",
        data: {{oprefs | safe}},
        backgroundColor: 'rgb(255, 235, 59, 0.5)',
        borderColor: 'rgb(255, 235, 59)',
        borderWidth: 2,
        pointBackgroundColor: 'rgb(255, 235, 59)'
      }
    ]
  },
  options: {
    scale: {ticks: {
            min:0,
            }
    },
    scales: {
        xAxes: [{
              display: false,
            gridLines: {
                display:false
            }
        }],
        yAxes: [{
          display: false,
            gridLines: {
                display:false
            }
        }]
    },
     title: {
        display: true,
        text: 'Opp Shot Distribution Chart'
    },
    responsive: true,
    animation: {duration:2000}
  }
});
     new Chart(document.getElementById("goodstuff"), {
  "type": "horizontalBar",
  "data": {
    "labels": {{goodtitles | safe}},
    "datasets": [{
      "label": "Positive Actions",
      "data": {{goodvalues | safe}},
      "fill": false,
      "backgroundColor": ['rgb(63, 81, 181, 1.0)', 'rgb(63, 81, 181, 0.85)',
                         'rgb(63, 81, 181, 0.70)', 'rgb(63, 81, 181, 0.55)',
                         'rgb(63, 81, 181, 0.45)'],
      "borderColor": 'rgb(63, 81, 181, 1.0)',
    }],
  },
  "options": {
    "scales": {
      "xAxes": [{
        scaleLabel: {
          display: true,
          labelString: "Correlation to Winning"
        },
        "ticks": {
          "beginAtZero": true,
          max: 1.0
        }
      }],
      yAxes: [{
        display: true,
        gridLines: {
          display:false
        }
      }],
    },
     title: {
        display: true,
        text: 'Top 5 Positive Actions'
    },
     legend: {
        display: false},
    responsive: true,
    animation: {duration:2000}
  }
});
     new Chart(document.getElementById("badstuff"), {
  "type": "horizontalBar",
  "data": {
    "labels": {{badtitles | safe}},
    "datasets": [{
      "label": "Negative Actions",
      "data": {{badvalues | safe}},
      "fill": false,
      "backgroundColor": ['rgb(255, 235, 59, 1.0)', 'rgb(255, 235, 59, 0.85)',
                         'rgb(255, 235, 59, 0.70)', 'rgb(255, 235, 59, 0.55)',
                         'rgb(255, 235, 59, 0.40)'],
      "borderColor": 'rgb(255, 235, 59, 1.0)',
    }],
  },
  "options": {
    "scales": {
      "xAxes": [{
        scaleLabel: {
          display: true,
          labelString: "Correlation to Winning"
        },
        "ticks": {
          "beginAtZero": true,
          min: -1.0
        }
      }],
      yAxes: [{
        display: true,
        position: 'right',
        gridLines: {
          display:false
        }
      }],
    },
     title: {
        display: true,
        text: 'Top 5 Negative Actions'
    },
     legend: {
        display: false},
    responsive: true,
    animation: {duration:2000}
  }
});
