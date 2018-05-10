$('#launch').click(function(){
    var text = $.get('tweets', {'query': $('#query').val()}, function(data){
    text_string=' ';
    var texts = data['server_to_client_data']
    for(i=0; i<texts.length; i++){
        text_string+=texts[i].text;
    }
    buildChart(text_string);
});

});

function buildChart(text_string){
var lines = text_string.split(/[,. ]+/g),
  data = Highcharts.reduce(lines, function (arr, word) {
    var obj = Highcharts.find(arr, function (obj) {
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

  series: [{
    type: 'wordcloud',
    data: data,
    name: 'Occurrences',
    spiral: 'archimedean'
  }],
  title: {
    text: '@' + $('#query').val() + '\'s' + ' last 50 tweets and retweets:'
  },

});
};