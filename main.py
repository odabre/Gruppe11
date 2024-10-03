from flask import Flask
from datetime import datetime
from time import time

# Create an instance of the Flask class
app = Flask(__name__)



# Define a route for the home page
@app.route('/')
def home():
    html = "<h1>Andreas er bedre enn Nicolai</h1><p>Denne nettsiden inneholder fakta</p>"
    
    currentDateAndTime = datetime.now()

    html += "The current date and time is  " + str(currentDateAndTime)
    for i in range(100):
        html += "<h3>Dette er linje nr: " + str(i) + "<h3>"
    return html

# Define a route for a custom page
@app.route('/about')
def about():
    return "NicolaiErBadass"
    #return render_template("nicolaiermegabadassogkjekk.html")

# Run the application
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5502, debug=True)
