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
import time
from threading import Thread
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



tds_liste_synkron = []
timestamp_tds = []
tds_verdi_graf = 2
def generate_data():
        global data_graf_tds
        while True:
            tds_verdi_graf =  random.randint(-10,10)
            tds_liste_synkron.append(tds_verdi_graf)
            timestamp_tds.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if len(tds_liste_synkron)>100:
                tds_liste_synkron.pop(0)
                timestamp_tds.pop(0)
            
            data_graf_tds = {
                "tds": tds_liste_synkron,
                "timestamp": timestamp_tds
                }
            time.sleep(1)
thread = Thread(target=generate_data)
thread.daemon = True  # Tråden stopper når Flask stopper
thread.start()

temperatur_liste_synkron = []
timestamp_temperatur = []
temperatur_verdi_graf = 2
def generate_data_temperatur():
        global data_graf_temperatur
        while True:
            temperatur_verdi_graf =  random.randint(-10,10)
            temperatur_liste_synkron.append(temperatur_verdi_graf)
            timestamp_temperatur.append(datetime.datetime.now().strftime("%H:%M:%S"))
            if len(temperatur_liste_synkron)>100:
                temperatur_liste_synkron.pop(0)
                timestamp_temperatur.pop(0)
            
            data_graf_temperatur = {
                "temperatur": temperatur_liste_synkron,
                "timestamp": timestamp_temperatur
                }
            time.sleep(2)
thread = Thread(target=generate_data_temperatur)
thread.daemon = True  # Tråden stopper når Flask stopper
thread.start()

turbiditet_liste_synkron = []
timestamp_turbiditet = []
turbiditet_verdi_graf = 2
def generate_data_turbiditet():
        global data_graf_turbiditet
        while True:
            turbiditet_verdi_graf =  random.randint(-10,10)
            turbiditet_liste_synkron.append(turbiditet_verdi_graf)
            timestamp_turbiditet.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if len(turbiditet_liste_synkron)>100:
                turbiditet_liste_synkron.pop(0)
                timestamp_turbiditet.pop(0)
            
            data_graf_turbiditet = {
                "turbiditet": turbiditet_liste_synkron,
                "timestamp": timestamp_turbiditet
                }
            time.sleep(1)
thread = Thread(target=generate_data_turbiditet)
thread.daemon = True  # Tråden stopper når Flask stopper
thread.start()


ph_liste_graf = []
timestamp_ph_graf = []
ph_liste_fil = []
timestamp_ph_fil = [] 
def oppdater_lister_fil(liste, tid_liste):
        verdi = random.randint(-10,10)
        liste.append(verdi)
        tid_liste.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(liste)>10:
            liste.pop(0)
            tid_liste.pop(0)
        data = {
            "verdi": liste,
            "timestamp": tid_liste
            }
        return data, liste, tid_liste
turbiditet_liste_graf = []
timestamp_turbiditet_graf = []
turbiditet_liste_fil = []
timestamp_turbiditet_fil = []

temperatur_liste_graf = []
timestamp_temperatur_graf = []
temperatur_liste_fil = []
timestamp_temperatur_fil = []


@app.route('/')
def run():
    return render_template("test.html")


@app.route('/ph')
def oda_func():
    return render_template("ph.html")
@app.route('/download_ph_csv')
def download_ph_csv():
    # Generer DataFrame
    global ph_liste_fil, timestamp_ph_fil
    ph_data_fil, ph_liste_fil, timestamp_ph_fil = oppdater_lister_fil(ph_liste_fil, timestamp_ph_fil)
    ph_data_fil = pd.DataFrame(ph_data_fil)
    # Lagre DataFrame som CSV i minnet (StringIO)
    csv_data_ph = BytesIO()
    ph_data_fil.to_csv(csv_data_ph, index=False)
    csv_data_ph.seek(0)  # Sett tilbake filpekeren til starten

    # Send CSV-filen som et vedlegg
    return send_file(csv_data_ph, mimetype='text/csv', as_attachment=True, download_name="data.csv")
@app.route('/update_ph')
def update_ph():
    global ph_liste_graf, timestamp_ph_graf
    # Genererer et tilfeldig tall (eller annen dynamisk data)
    data_ph_graf, ph_liste_graf, timestamp_ph_graf = oppdater_lister_fil(ph_liste_graf, timestamp_ph_graf)
    # Returnerer dataen i JSON-format
    return jsonify(data_ph_graf)


@app.route('/temperatur')
def chello_func():
    return render_template("temperatur.html")
@app.route('/download_temperatur_csv')
def download_temperatur_csv():
    # Generer DataFrame
    temperatur_data_fil = pd.DataFrame(data_graf_temperatur)
    # Lagre DataFrame som CSV i minnet (StringIO)
    csv_data_temperatur = BytesIO()
    temperatur_data_fil.to_csv(csv_data_temperatur, index=False)
    csv_data_temperatur.seek(0)  # Sett tilbake filpekeren til starten

    # Send CSV-filen som et vedlegg
    return send_file(csv_data_temperatur, mimetype='text/csv', as_attachment=True, download_name="data.csv")

@app.route('/update_temperatur')
def update_temperatur():
    return jsonify(data_graf_temperatur)


@app.route('/sensor')
def sensor_func():
    return render_template("sensor.html")
@app.route('/download_tds_csv')
def download_tds_csv():
    # Generer DataFrame
    tds_liste_fil = pd.DataFrame(data_graf_tds)

    # Lagre DataFrame som CSV i minnet (StringIO)
    csv_data_tds = BytesIO()  
    tds_liste_fil.to_csv(csv_data_tds, index=False)
    csv_data_tds.seek(0)  # Sett tilbake filpekeren til starten

    # Send CSV-filen som et vedlegg
    return send_file(csv_data_tds, mimetype='text/csv', as_attachment=True, download_name="data.csv")

@app.route('/update_tds')
def update_tds():
    # Genererer et tilfeldig tall (eller annen dynamisk data)
    # Returnerer dataen i JSON-format
    return jsonify(data_graf_tds)



@app.route('/turbiditet')
def nr1_func():
    return render_template("turbiditet.html")
@app.route('/download_turbiditet_csv')
def download_turbiditet_csv():
    # Generer DataFrame
    turbiditet_data_fil = pd.DataFrame(data_graf_turbiditet)
    # Lagre DataFrame som CSV i minnet (StringIO)
    csv_data_turbiditet = BytesIO()
    turbiditet_data_fil.to_csv(csv_data_turbiditet, index=False)
    csv_data_turbiditet.seek(0)  # Sett tilbake filpekeren til starten

    # Send CSV-filen som et vedlegg
    return send_file(csv_data_turbiditet, mimetype='text/csv', as_attachment=True, download_name="data.csv")
@app.route('/update_turbiditet')
def update_turbiditet():
    # Returnerer dataen i JSON-format
    return jsonify(data_graf_turbiditet)





#function that we can call from other scripts to run the server in case we want to run the server even if __name__ != '__main__'
def run_app():
    app.run(host="0.0.0.0", port=5502, debug=True)
    
# Run the application
if __name__ == '__main__':
    run_app()

#  git config --global user.email "you@example.com"
#  git config --global user.name "Your Name"



