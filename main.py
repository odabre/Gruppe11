from flask import Flask
from datetime import datetime
from time import time
import chello
import oda
# Create an instance of the Flask class
app = Flask(__name__)



# Define a route for the home page
@app.route('/')
def home():
    html = "<h1>Andreas er mye bedre enn Nicolai</h1><p>Denne nettsiden inneholder fakta</p>"
    html += "<h2>Men Johanne og gruppe 9 er bes!<h2>"
    html += """<a href="oda"> Oda</a> <a href="chello"> chello </a>"""
    
    currentDateAndTime = datetime.now()

    html += "The current date and time is  " + str(currentDateAndTime)
    for i in range(1,101):
        html += "<h3>Dette er linje nr: " + str(i) + "<h3>"
    
    return html 

# Define a route for a custom page
@app.route('/about')
def about():
    return "NicolaiErBadass"
    #return render_template("nicolaiermegabadassogkjekk.html")

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
