from flask import Flask, render_template, request, Response
import serial, time, pymysql

import pandas as pd
import json
import plotly
import plotly.graph_objects as go

connection = pymysql.connect(host='localhost',
                             user='root', 
                             password='qwerty',
                             database='app_weather')
cursor = connection.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    cursor.execute('SELECT id, dato_sensor, sensor_id, created_at FROM historial WHERE sensor_id=1')
    tempeData = cursor.fetchall()

    cursor.execute('SELECT id, dato_sensor, sensor_id, created_at FROM historial WHERE sensor_id=2')
    presionData = cursor.fetchall()

    cursor.execute('SELECT id, dato_sensor, sensor_id, created_at FROM historial WHERE sensor_id=3')
    altitudData = cursor.fetchall()

    xT = []
    yT = []
    for row in tempeData:
        xT.append(row[3])
        yT.append(row[1])

    xP = []
    yP = []
    for row in presionData:
        xP.append(row[3])
        yP.append(row[1])

    xA = []
    yA = []
    for row in altitudData:
        xA.append(row[3])
        yA.append(row[1])

    # Create Bar chart
    figT = go.Figure()
    figT.add_trace(go.Scatter(x=xT,y=yT,mode='lines',name='Datos'))

    figP = go.Figure()
    figP.add_trace(go.Scatter(x=xP,y=yP,mode='lines',name='Datos'))

    figA = go.Figure()
    figA.add_trace(go.Scatter(x=xA,y=yA,mode='lines',name='Datos'))

    # Create graphJSON
    graphJSONT = json.dumps(figT, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSONP = json.dumps(figP, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSONA = json.dumps(figA, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Use render_template to pass graphJSON to html
    return render_template('index.html', graphJSONT=graphJSONT,graphJSONP=graphJSONP,graphJSONA=graphJSONA)

@app.route('/recibir-datos', methods=['POST'])
def recibir_datos():
    arduino = serial.Serial('COM3', 9600)
    while True:
        time.sleep(5)
        data = arduino.readline()
        arrayData = data.split()

        temperature = float(arrayData[0].decode('utf-8'))
        presion = float(arrayData[1].decode('utf-8'))
        altitud = float(arrayData[2].decode('utf-8'))

        queryTemp = "INSERT historial (dato_sensor,created_at,sensor_id) VALUES (%s,now(),1)" %temperature
        cursor.execute(queryTemp)

        queryPresion = "INSERT historial (dato_sensor,created_at,sensor_id) VALUES (%s,now(),2)" %presion
        cursor.execute(queryPresion)

        queryAltitud = "INSERT historial (dato_sensor,created_at,sensor_id) VALUES (%s,now(),3)" %altitud
        cursor.execute(queryAltitud)

        connection.commit()
    return {
        "temperature": queryTemp,
        "presion": queryPresion,
        "altitud": queryAltitud
    }

@app.route('/mostrar-datos')
def dibuja_grafico():
    cursor.execute('SELECT historial.id, sensor.name_sensor, historial.created_at FROM sensor RIGHT JOIN historial ON sensor.id = historial.sensor_id;')
    datas = cursor.fetchall()
    print(datas)
    
    return render_template('datos.html', datas=datas) 

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
