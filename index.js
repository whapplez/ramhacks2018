const express = require('express');
const app = express();
const Twitter = require('twitter');
const request = require('request');
const http = require('http');

const con_key = "PLpOT57q5n8BwYrpm8u8Z9ROf";
const con_secret = "EI0azViZNaqWjXBaSdLNKz89ohtkP9vP9FgddKoXBMuDS5VdGK";
var bear2 = "UExwT1Q1N3E1bjhCd1lycG04dThaOVJPZjpFSTBhelZpWk5hcVdqWEJhU2RMTkt6ODlvaHRrUDl2UDlGZ2RkS29YQk11RFM1VmRHSw==";
var tweetarry = [];
var accarray = ["uvadining", "uvaesc", ];
var client = new Twitter({
	consumer_key: con_key,
	consumer_secret: con_secret,
	bearer_token: "AAAAAAAAAAAAAAAAAAAAAIQX8gAAAAAAWY37UqYee%2BxEQBVGMIrZ4AexiRk%3DVFOXMzdSYt9o8JaRTcowei5DlBow5RFbeRnVoNtaFCthe5RDta"
});

app.set('port', process.env.PORT || 8080 );

app.get('/', function(req, res){
    var spawn = require('child_process').spawn;
	var py = spawn('python', ['compute_input.py', req.query.firstName, req.query.lastName]);

	py.stdout.on('data', function(data) { 
    	res.send(data.toString()); 
	}) ;

});

var arry2 = new Promise(function(resolve, reject){
	var params = {screen_name: 'uvaesc', count:20, tweet_mode: 'extended'};

	client.get('search/tweets', {q: 'free food uva', tweet_mode: 'extended'}, function(error, tweets, response){
		if(!error){
			for(i in tweets.statuses){
				tweetarry.push({
					name: tweets.statuses[i].user.name,
					date: tweets.statuses[i].created_at,
					text: tweets.statuses[i].full_text
				});
			}
			resolve(tweetarry);
		}
		else{
			console.log(error)
		}
	});
});

arry2.then(function(fulfilled){
	//console.log(fulfilled)
});

var listener = app.listen(app.get('port'), function() {
  console.log( 'Express server started on port: '+listener.address().port );
});