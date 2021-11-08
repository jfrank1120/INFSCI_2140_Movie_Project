from flask import Flask, redirect


import datetime
import json


app = Flask(__name__)

@app.route('/')
def root():
    return redirect("/static/index.html", code=302)


# startTime = datetime.datetime.now()
# PreProcess("trecweb")
# endTime = datetime.datetime.now()
# print ("index text corpus running time: ", endTime - startTime)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
