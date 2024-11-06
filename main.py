from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime
from time import time
from threading import Timer
import numpy as np
import pandas as pd
import datetime
import csv
import random
import chello
import oda
import os
from io import StringIO
from io import BytesIO
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
tds_liste = []
def uppdate_list_fil_tds():
        tds_verdi = esp32_data["tdsverdi"]
        tds_liste.append(tds_verdi)
        timestamp.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(tds_liste)>10:
            tds_liste.pop(0)
            timestamp.pop(0)
        tds_data = {
            "tds": tds_liste,
            "timestamp": timestamp
            }
        print(tds_data)

        
        return pd.DataFrame(tds_data)
def uppdate_list_graf_tds():
        tds_verdi_graf = esp32_data["tdsverdi"]
        tds_liste.append(tds_verdi_graf)
        timestamp.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(tds_liste)>10:
            tds_liste.pop(0)
            timestamp.pop(0)
        data_graf_tds = {
            "tds": tds_liste,
            "timestamp": timestamp
            }
        return data_graf_tds
temperatur_liste_graf = []
timestamp_temp_graf = []
def uppdate_list_graf_temperatur():
        temperatur_verdi = random.randint(-10,10)
        temperatur_liste_graf.append(temperatur_verdi)
        timestamp_temp_graf.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(temperatur_liste_graf)>10:
            temperatur_liste_graf.pop(0)
            timestamp_temp_graf.pop(0)
        data_graf_temperatur = {
            "temperatur": temperatur_liste_graf,
            "timestamp": timestamp_temp_graf
            }
        return data_graf_temperatur
temperatur_liste_fil = []
timestamp_temp_fil = []
def uppdate_list_fil_temperatur():
        temperatur_verdi = random.randint(-10,10)
        temperatur_liste_fil.append(temperatur_verdi)
        timestamp_temp_fil.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(temperatur_liste_fil)>10:
            temperatur_liste_fil.pop(0)
            timestamp_temp_fil.pop(0)
        data_fil_temperatur = {
            "tds": temperatur_liste_fil,
            "timestamp": timestamp_temp_fil
            }
        return pd.DataFrame(data_fil_temperatur)

@app.route('/')
def run():
    return render_template("test.html")


@app.route('/ph')
def oda_func():
    return render_template("ph.html")


@app.route('/temperatur')
def chello_func():
    return render_template("temperatur.html")
@app.route('/download_temperatur_csv')
def download_temperatur_csv():
    # Generer DataFrame
    temperatur_liste_fil = uppdate_list_fil_temperatur()

    # Lagre DataFrame som CSV i minnet (StringIO)
    csv_data_temperatur = BytesIO()
    temperatur_liste_fil.to_csv(csv_data_temperatur, index=False)
    csv_data_temperatur.seek(0)  # Sett tilbake filpekeren til starten

    # Send CSV-filen som et vedlegg
    return send_file(csv_data_temperatur, mimetype='text/csv', as_attachment=True, download_name="data.csv")

@app.route('/update_temperatur')
def update_temperatur():
    # Genererer et tilfeldig tall (eller annen dynamisk data)
    data_temperatur_graf = uppdate_list_graf_temperatur()
    # Returnerer dataen i JSON-format
    return jsonify(data_temperatur_graf)


@app.route('/sensor')
def sensor_func():
    return render_template("sensor.html")
@app.route('/download_tds_csv')
def download_tds_csv():
    # Generer DataFrame
    tds_liste_fil = uppdate_list_fil_tds()

    # Lagre DataFrame som CSV i minnet (StringIO)
    csv_data_tds = BytesIO()
    tds_liste_fil.to_csv(csv_data_tds, index=False)
    csv_data_tds.seek(0)  # Sett tilbake filpekeren til starten

    # Send CSV-filen som et vedlegg
    return send_file(csv_data_tds, mimetype='text/csv', as_attachment=True, download_name="data.csv")

@app.route('/update_tds')
def update_tds():
    # Genererer et tilfeldig tall (eller annen dynamisk data)
    datagraf = uppdate_list_graf_tds()
    # Returnerer dataen i JSON-format
    return jsonify(datagraf)



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



