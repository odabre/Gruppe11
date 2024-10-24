from flask import Flask, render_template
from datetime import datetime
from time import time
import chello
import oda
import os
# Create an instance of the Flask class
app = Flask(__name__)

@app.route('/')
def run():
    return render_template("test.html")


lol = ["nicolai", "oda", "chello"]

@app.route('/oda')
def oda_func():
    return render_template("oda.html", liste = lol)


@app.route('/temperatur')
def chello_func():
    return render_template("temperatur.html")


@app.route('/sensor')
def sensor_func():
    return render_template("sensor.html")

@app.route('/turbiditet')
def nr1_func():
    return render_template("turbiditet.html")

@app.route('/nr2')
def nr2_func():
    return render_template("nr2.html")

# Run the application
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5502, debug=True)

#  git config --global user.email "you@example.com"
#  git config --global user.name "Your Name"



