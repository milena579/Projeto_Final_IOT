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

def startDatabase(tools):
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

        ],"tools":tools,
        "lend":-1
    }
    db.reference("/").set(data)

def pushDatabase(data):
    db.reference("/tools").set(data)

def captureImage():
    cap = cv2.VideoCapture(0)
    try:
        status, photo = cap.read()
        photo = cv2.resize(photo, (640, 640))
        cv2.imwrite("image.png", photo)
        return "image.png"
    finally:
        cap.release()

def readSerial(ser):
    line = ser.readline()
    line = line.decode('utf-8')
    return line

def updateTools(tools):
    result = model.predict(captureImage())    
    for box in  result[0].boxes:
        if(float(box.conf)>0.5):
            tools[int(box.cls)]["qta"]+=1
    pushDatabase(tools)
    return tools

def updateLending(data):
    db.reference("/lend").push(data)

def resetTools():
    return [
        {
            "name":"Hammer",
            "qta":0
        },
        {
            "name":"Pliers",
            "qta":0
        },
        {
            "name":"screwdriver",
            "qta":0
        },
        {
            "name":"wrench",
            "qta":0
        }
    ]

connectFirebase()
ser = startSerial()
model = startModel()




firstools = updateTools(resetTools())
startDatabase(firstools)


oldLine = ""

while 1:
    tools = resetTools()

    line = readSerial(ser)
    print(line)

    if(line != "" or line!=oldLine):
        oldLine = line
        time.sleep(2)
        result = model.predict(captureImage())    
        for box in  result[0].boxes:
            if(float(box.conf)>0.5):
                tools[int(box.cls)]["qta"]+=1
        pushDatabase(tools)
    
    toolLend=""

    for i in range(4):
        num = firstools[i]["qta"] - tools[i]["qta"]
        if(num>0):
            toolLend += num+"x"+tools[i]["name"] if i==0 else ", "+num+"x"+tools[i]["name"]
    if(toolLend==""):
        continue
    updateLending({"RFID":line,"loan":toolLend})


        
        