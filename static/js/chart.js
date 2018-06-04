$(function() {
    tweets('realdonaldtrump');
    $('#launch').click(function() {
        tweets($('#query').val());
    });
});

function tweets(query) {
    $('.panel-group').empty();
    var query = query;
    $.get('tweets', {
        'query': query
    }, function(data) {
        data = data['tweets'];
        clean = '';
        for (i = 0; i < data.length; i++) {
            clean += data[i]['clean'];
            $('.pre-scrollable').append('<div class="panel-group">' + n() + '</div>');
        }

        function n() {
            if (data[i]['sentiment'] == 'positive') {
                return '<div class="panel panel-success">' + '<div class="panel-heading">' + '@ ' + data[i]['username'] + '</div>' + '<div class="panel-body">' + data[i]['text'] + '</div>' + '</div>';
            } else if (data[i]['sentiment'] == 'negative') {
                return '<div class="panel panel-danger">' + '<div class="panel-heading">' + '@ ' + data[i]['username'] + '</div>' + '<div class="panel-body">' + data[i]['text'] + '</div>' + '</div>';
            } else {
                return '<div class="panel panel-default">' + '<div class="panel-heading">' + '@ ' + data[i]['username'] + '</div>' + '<div class="panel-body">' + data[i]['text'] + '</div>' + '</div>';
            }
        };

        buildChart(clean);
    });
};

function buildChart(clean) {
    var lines = clean.split(/[,. ]+/g),
        data = Highcharts.reduce(lines, function(arr, word) {
            var obj = Highcharts.find(arr, function(obj) {
                return obj.name === word;
            });
            if (obj) {
                obj.weight += 1;
            } else {
                obj = {
                    name: word,
                    weight: 1
                };
                arr.push(obj);
            }
            return arr;
        }, []);
    Highcharts.chart('container', {
        chart: {
            type: 'wordcloud',
            //      backgroundColor: '#F4F6F6',
        },
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 1600,
                    maxHeight: 1600
                }
            }]
        },
        series: [{
            type: 'wordcloud',
            borderSize: '10px',
            data: data,
            name: 'Frequency'
            //    spiral: 'archimedean'
        }],
        title: {
            text: 'from ' + '@' + $('#query').val() + '\'s' + ' last 50 tweets and retweets:'
        },
    });
};
