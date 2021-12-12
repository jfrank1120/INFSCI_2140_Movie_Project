import flask
import demjson
from flask import Flask, redirect, Response, session
from main_actions import SearchforMovie

import json


app = Flask(__name__)
app.secret_key = b'@U\xb0\xadf\x92f\xe8\x10\xee\xdf\x81O\x92\xb7\xe5\xca\x10rE&=\xd0\x7f'

dummyClass = SearchforMovie()
similar_search_class = SearchforMovie()
filter_search_class = SearchforMovie()

@app.route('/')
def root():
    return redirect("/static/index.html", code=302)

@app.route('/search', methods=['POST'])
def query():
    # Pull query from front-end
    search_query = flask.request.form['query']
    # Pull filters from front-end
    filters = flask.request.form['filters']
    # Check for a year filter
    #year = flask.request.form['year']
    # Add searh to list of previous searches
    try:
        if not session['prev_searches'].__contains__(search_query):
            session['prev_searches'] = session['prev_searches'] + [search_query]
    except:
        session['prev_searches'] = [search_query]

    print(session['prev_searches'])
    filter_dict = demjson.decode(filters)
    dummyClass.set_query(search_query)
    result = dummyClass.retrieve(topK=10)
    origin_filter = result
    for key, value in filter_dict.items():
        if value:
            print('filtering on: ' + key)
            origin_filter = filter_search_class.filter_results_by_origin(result, key)

    return Response(json.dumps(origin_filter), mimetype='application/json')


@app.route('/get_similar', methods=['POST'])
def get_similar():
    movie_title = flask.request.form['movie_title']
    print("Getting similar : " + movie_title)
    similar_results = dummyClass.get_similar(movie_title)
    print(similar_results)
    session['similar_results'] = similar_results
    session['curr_sim_movie'] = movie_title
    try:
        session['searched_movies'] = session['searched_movies'] + [movie_title]
    except:
        session['searched_movies'] = [movie_title]
    return Response(json.dumps(similar_results), mimetype='application/json')

@app.route('/get_similar_results', methods=["POST"])
def get_similar_results():
    print(session['similar_results'])
    sim_json = {
        'similar_results': session['similar_results'],
        'movie_title': session['curr_sim_movie']
    }
    return Response(json.dumps(sim_json), mimetype='application/json')

@app.route('/populate_user_data', methods=['POST'])
def populate_user_data():
    # TODO - Pull data from the file with user data and send to the front end
    print('Getting user data')

@app.route('/get_recs', methods=['POST'])
def get_recs():
    results = []
    try:
        if len(session['searched_movies']) != 0:
            results = dummyClass.get_recommendation_by_past_search(session['searched_movies'])
    except:
        results = []
    return Response(json.dumps(results), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
