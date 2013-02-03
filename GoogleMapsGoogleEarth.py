'''
IO Experiment 4

Caberio
Cacalda
Decano
Gonzales

'''
import sys
import os
import serial

import time
from Tkinter import *
from googlemaps import GoogleMaps

gmaps = GoogleMaps(api_key = "AIzaSyD4qJM8Ai8dl3hTxvf_CiCimDWbFHdHey8")

SerialPort = serial.Serial("COM29",115200)
buf = ''
SerialPort.write('AT+CMGF=1\r\n')
time.sleep(1)
r1= SerialPort.read(SerialPort.inWaiting())
print r1
x = "OK" in r1

if x == True:
    print "Step1"
    buf = buf+r1
    print buf
    y = "OK" in buf
    if y == True:
        print "Step2"
        SerialPort.write('AT+CMGR=0\r\n')
        time.sleep(1)
        r2 = SerialPort.read(SerialPort.inWaiting())
        buf = buf+r2
        print buf
        buf1 = buf.split()

        lat = buf1[4]
        lng = buf1[5]
        u = buf1[3]
        splitsender = u.split(',')

        sender = splitsender[1]
        print 'Latitude = '+lat
        print 'Longitude = ' +lng
        print "Sender = "+sender
        LAT = float(lat)
        LNG = float(lng)

        SerialPort.write('AT+CMGD=0\r\n')    

        print "Loading address from Google Maps \n Please wait..."
        destination = gmaps.latlng_to_address(LAT, LNG)

        print "Ikaw ay papunta sa\n"+destination

        SerialPort.write('AT+CMGS='+sender+'\r\n')
        time.sleep(1)
        print SerialPort.read(SerialPort.inWaiting())
        time.sleep(1)
        SerialPort.write(destination+'\x1A')
        print SerialPort.read(SerialPort.inWaiting())
        time.sleep(1)
        print 'Confirmation Message Sent'

        print'Loading google earth.....'
        import win32com.client
        ge = win32com.client.Dispatch("GoogleEarth.ApplicationGE")
        time.sleep(5)
        latitude = LAT
        longitude= LNG
        altitude = 1000
        altMode = 1
        focusDistance =3000
        tilt = 0
        azimuth = 370
        speed = 0.5
        time.sleep(4)
        ge.SetCameraParams (latitude, longitude, altitude, altMode, focusDistance, tilt, azimuth, speed)

        #added code
        app = Tk()
        app.title('IO Experiment 4: Coordinates to Address')
        app.geometry('450x300+350+400')

        labeltext = StringVar()
        labeltext.set("Latitude: "+lat + "\nLongitude: "+lng+"\nLocation: " +destination +"\nThe address was sent to: "+sender)
        label1 = Label(app, textvariable = labeltext, height =20)
        label1.pack()
        app.mainloop()


