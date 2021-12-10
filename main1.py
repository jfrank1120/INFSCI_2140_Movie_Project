import flask
from flask import Flask, redirect, Response
from main_actions import SearchforMovie

import json


app = Flask(__name__)
dummyClass = SearchforMovie()

@app.route('/')
def root():
    return redirect("/static/index.html", code=302)

@app.route('/search', methods=['POST'])
def query():
    # Pull query from front-end
    # search_query = flask.Request.form['query']
    # Pull filters from front-end
    # filters = flask.Request.form['filters']
    

    # data = search()
    dummyClass.set_query("city action jump")
    result = dummyClass.retrieve(topK=10)
    
    return Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
