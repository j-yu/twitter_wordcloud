from flask import Flask, render_template, request, jsonify
from flask_bower import Bower
from twitter_client import TwitterInterface


app = Flask(__name__)
Bower(app)

client = TwitterInterface()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tweets')
def tweets():
    incoming = request.args.get('query')
    client.screen_name = incoming
    data = client.grab_texts()

    return jsonify({'tweets': [i for i in data]})
