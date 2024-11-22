import matplotlib.pyplot as plt
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import serial
import time
from ultralytics import YOLO
import numpy as np
import cv2
from datetime import datetime

def connectFirebase():
    cred = credentials.Certificate("servico.json")
    firebase_admin.initialize_app(cred,{'databaseURL': 'https://iot-final-23bc2-default-rtdb.firebaseio.com'})

def startSerial():
    return serial.Serial('COM6', 9600, timeout=1)

def startModel():
    return YOLO("Rede1/best.pt")

def startDatabase(tools,employers):
    data = {"employers":employers,"tools":tools,
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
            "name":"Martelo",
            "qta":0
        },
        {
            "name":"Alicate",
            "qta":0
        },
        {
            "name":"Chave de fenda",
            "qta":0
        },
        {
            "name":"Chave de boca",
            "qta":0
        }
    ]


connectFirebase()
ser = startSerial()
model = startModel()

employers = [
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
    {
        "name":"Adrian",
        "EDV":"08A7060D",
        "RFID":"08A7060D"
    }
]



firstools = updateTools(resetTools())
startDatabase(firstools,employers)


oldLine = ""

while 1:
    tools = resetTools()

    line = readSerial(ser)

    if(line != "" and line!=oldLine):
        print(line)
        oldLine = line
        rfid = line.strip()
        while True:
            line = readSerial(ser)
            if(line.strip()=="closed"):
                oldLine = line
                break
        time.sleep(2)
        result = model.predict(captureImage())    
        for box in  result[0].boxes:
            if(float(box.conf)>0.3):
                tools[int(box.cls)]["qta"]+=1
        pushDatabase(tools)
    
        toolLend=""
        toolReturn=""

        for i in range(len(firstools)):
            num = firstools[i]["qta"] - tools[i]["qta"]
            print(str(num)+"="+str(firstools[i]["qta"])+"-"+str(tools[i]["qta"]))
            if(num>0):
                toolLend +=str(num)+"x"+tools[i]["name"] if toolLend=="" else ", "+str(num)+"x"+tools[i]["name"]
                continue
            if(num<0):
                toolReturn +=str(num*-1)+"x"+tools[i]["name"] if toolReturn=="" else ", "+ str(num*-1)+"x"+tools[i]["name"]

        if(toolLend=="" and toolReturn==""):
            continue
        
        send = False
        currtime = datetime.now()
        for i in range(len(employers)):
            if(employers[i]["RFID"] == rfid):
                updateLending({"name":employers[i]["name"],"RFID":rfid,"loan":toolLend,"return":toolReturn,"datetime":str(currtime)})
                print({"name":employers[i]["name"],"RFID":rfid,"loan":toolLend,"return":toolReturn,"datetime":str(currtime)})
                send=True
        if(not send):
            updateLending({"name":"Desconhecido","RFID":rfid,"loan":toolLend,"return":toolReturn,"datetime":str(currtime)})
            print({"name":"Desconhecido","RFID":rfid,"loan":toolLend,"return":toolReturn,"datetime":str(currtime)})

        firstools = tools


        
        