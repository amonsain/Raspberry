#!/usr/bin/env python

import sqlite3

import time
import math


# global variables
speriod=(1)
dbname='/var/www/weatherlog.db'



# store the Pressure in the database
def log_pressure(press):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO Pressure values(datetime('now'), (?))", (press,))

    # commit the changes
    conn.commit()

    conn.close()


# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM Pressure"):
        print str(row[0])+" "+str(row[1])

    conn.close()



# get Pressure
# returns the Pressure as a float, compensated to sea level
def get_press(altitude):

 # enable SenseHat modules
    from sense_hat import SenseHat
    
    sense=SenseHat()
    raw_pressure1 = sense.get_pressure()
    time.sleep(0.1) 
    raw_pressure2 = sense.get_pressure()
    time.sleep(0.1) 
    raw_pressure3 = sense.get_pressure()
    raw_pressure=(raw_pressure1+raw_pressure2+raw_pressure3)/3
    pressure = raw_pressure/math.pow(1 - 0.0065*altitude/288.15,5.25588)
    #print(pressure)
    return pressure


# main function
# This is where the program starts 
def main():


    while True:

    # get the pressure from SenseHat and Store it
        pressure = get_press(150)
        if pressure != None:
            print "Pressure="+str(pressure)
            #log_pressure(pressure)
        else:
            print "Error getting Pressure"

        # Store the temperature in the database
    

        # display the contents of the database
#        display_data()

        time.sleep(speriod)


if __name__=="__main__":
    main()