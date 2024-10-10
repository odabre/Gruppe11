from flask import Flask
from datetime import datetime
from time import time
import chello
import oda
# Create an instance of the Flask class
app = Flask(__name__, static_folder='static')

@app.route('/')
def run():
    return """
    <html>
        <head>
            <title>Mausund</title>
            <style>
                body {
                    background-color: lightblue;
                }
            </style>
        </head>
        <body>
        </body>
    </html>
"""


@app.route('/oda')
def oda_func():
    return oda.run()


@app.route('/chello')
def chello_func():
    return chello.run()

# Run the application
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5502, debug=True)

#  git config --global user.email "you@example.com"
#  git config --global user.name "Your Name"



