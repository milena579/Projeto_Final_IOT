import matplotlib.pyplot as plt
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import serial
import time
from ultralytics import YOLO
import numpy as np
import cv2;


# ser = serial.Serial('COM6', 9600, timeout=1)
cred = credentials.Certificate("servico.json")
firebase_admin.initialize_app(cred,{
        'databaseURL': 'https://iot-final-23bc2-default-rtdb.firebaseio.com'
})
model = YOLO("best.pt")

ref = db.reference("/")

data = {"employers":
    [
        {
            "name":"Milena",
            "EDV":"99999999",
            "RFID":"C3018DAB"
        },
        {
            "name":"Ingrid",
            "EDV":"88888888",
            "RFID":"334D33AD"
        },
        {
            "name":"Juan",
            "EDV":"87888888",
            "RFID":"B3CA3310"
        },

    ],"tools":
    [
        {
            "name":"Hammer",
            "qta":"1"
        },
        {
            "name":"Pliers",
            "qta":"1"
        },
        {
            "name":"screwdriver",
            "qta":"1"
        },
        {
            "name":"wrench",
            "qta":"2"
        }
    ]
}

ref.set(data)

ref = db.reference("/lends")


oldline = ""

while 1:
    cap = cv2.VideoCapture(0)
    # line = ser.readline()
    # line = line.decode('utf-8')
    line = input("Line=")

    if(line!= "" or line!=oldline):
        oldline = line
        status, photo = cap.read()
        cap.release()
        photo_resized = cv2.resize(photo, (640, 640))
        # photo_array = np.expand_dims(photo_resized, axis=0)

        ref.push({"id":line})

        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        