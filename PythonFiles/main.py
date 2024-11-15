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

def connectFirebase():
    cred = credentials.Certificate("servico.json")
    firebase_admin.initialize_app(cred,{'databaseURL': 'https://iot-final-23bc2-default-rtdb.firebaseio.com'})

def startSerial():
    return serial.Serial('COM6', 9600, timeout=1)

def startModel():
    return YOLO("best.pt")

def startDatabase():
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
    db.reference("/").set(data)

def pushDatabase(data):
    ref = db.reference("/lends").push(data)

def captureImage():
    cap = cv2.VideoCapture(0)
    status, photo = cap.read()
    cap.release()
    photo_resized = cv2.resize(photo, (640, 640))
    return np.expand_dims(photo_resized, axis=0)

def readSerial(ser):
    line = ser.readline()
    line = line.decode('utf-8')










connectFirebase()
ser = startSerial()
model = startModel()
startDatabase()



oldLine = ""

while 1:
    line = readSerial(ser)

    if(line!= "" or line!=oldLine):
        oldLine = line

        result = model.predict(captureImage())
        
        print(result[0].names)
        for box in  result[0].boxes:
            print(box.cls,box.conf)

        pushDatabase({"info":result[0].boxes})

        
        