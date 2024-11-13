import matplotlib.pyplot as plt
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("servico.json")
firebase_admin.initialize_app(cred,{
        'databaseURL': 'https://iot-final-23bc2-default-rtdb.firebaseio.com'
})

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
            "EDV":"88888888",
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
            "qta":"1"
        }
    ]
}

ref.set(data)