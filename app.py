from flask import Flask, render_template, request, jsonify
from twitter_client import TwitterInterface

client = TwitterInterface()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweets')
def tweets():
    incoming = request.args.get('query')
    chosen_screen_name = incoming
    client.screen_name = chosen_screen_name
    server_to_client_data = client.grab_texts()
    return jsonify({'server_to_client_data': server_to_client_data})
