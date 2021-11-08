from flask import Flask, redirect, Response
from main_actions import search


import datetime
import json


app = Flask(__name__)

@app.route('/')
def root():
    return redirect("/static/index.html", code=302)

@app.route('/search', methods=['POST'])
def query():
    data = search()
    return Response(json.dumps(data), mimetype='application/json')

# startTime = datetime.datetime.now()
# PreProcess("trecweb")
# endTime = datetime.datetime.now()
# print ("index text corpus running time: ", endTime - startTime)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
