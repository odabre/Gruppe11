from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime
from time import time
from threading import Timer
import numpy as np
import csv
import random
import chello
import oda
import os
from io import StringIO
# Create an instance of the Flask class

app = Flask(__name__)


esp32_data = {"temperature": None, "tdsverdi": None}
tds_data = []

# Rute for å motta data fra ESP32
@app.route('/data', methods=['POST'])
def receive_data():
    global esp32_data  # Bruk global variabel for å lagre data
    data = request.json  # Hent JSON-data fra forespørselen
    if data:  # Hvis det er data i forespørselen
        esp32_data['temperature'] = data.get('temperature')  # Oppdater temperatur
        esp32_data['tdsverdi'] = data.get('tdsverdi')  # Oppdater fuktighet
        return jsonify({"message": "Data received successfully"}), 200  # Send suksessmelding
    return jsonify({"message": "No data received"}), 400  # Send feilmelding hvis ingen data


timestamp = []
random_list = []
def uppdate_random_list():
        global tds_data
        random_number = esp32_data["tdsverdi"]
        random_list.append(random_number)
        timestamp.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(random_list)>10:
            random_list.pop(0)
            timestamp.pop(0)
        tds_data = {
            "tds": random_list,
            "timestamp": timestamp
            }
        print(tds_data)

        
        return tds_data

@app.route('/')
def run():
    return render_template("test.html")


@app.route('/ph')
def oda_func():
    return render_template("ph.html")


@app.route('/temperatur')
def chello_func():
    return render_template("temperatur.html")


@app.route('/sensor')
def sensor_func():
    return render_template("sensor.html")
@app.route('/update')
def update_data():
    # Genererer et tilfeldig tall (eller annen dynamisk data)
    uppdate_random_list()
    # Returnerer dataen i JSON-format
    return jsonify(tds_data)
@app.route('/download-tds-data', methods=['GET'])
def download_tds_data():
    # Create a CSV file in memory
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["TDS", "Timestamp"])  # CSV header

    # Write each entry in `tds_data`
    for tds, timestamp in zip(tds_data["tds"], tds_data["timestamp"]):
        csv_writer.writerow([tds, timestamp])

    csv_file.seek(0)
    # Send the CSV file as an attachment
    return send_file(csv_file, mimetype='text/csv', as_attachment=True, download_name="tds_data.csv")

@app.route('/turbiditet')
def nr1_func():
    return render_template("turbiditet.html")

@app.route('/nr2')
def nr2_func():
    return render_template("nr2.html")

#function that we can call from other scripts to run the server in case we want to run the server even if __name__ != '__main__'
def run_app():
    app.run(host="0.0.0.0", port=5502, debug=True)
    
# Run the application
if __name__ == '__main__':
    run_app()

#  git config --global user.email "you@example.com"
#  git config --global user.name "Your Name"



