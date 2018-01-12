#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 1 19:32:32 2018

@author: Jonas K

A small sript to use Rejseplanen's public REST API. The output needs to fit
into Pythonista's terminal (40 characters on iPhone).
"""

import location
import requests
import sys
import datetime
import textwrap
import time
from conf import baseUrl, home1, work1


OUTPUTWIDTH = 40
GPSFACTOR   = 10**6


def requestStringTime(origin, dest, time):
    trip = [
        "/trip?originId=", str(origin),
        "&destId=", str(dest),
        "&time=", str(time),
        "&format=json"]
    return ''.join(trip)


def requestStringHome(lon, lat, dest, time):
    trip = [
        "/trip?originCoordX=", str(lon),
        "&originCoordY=", str(lat),
        "&originCoordName=Current_Location",
        "&destId=", str(dest),
        "&time=", str(time),
        "&format=json"]
    return ''.join(trip)


def durationString(trip):
#    print(trip)
    dep = trip[0]['Origin']['time']
    arr = trip[-1]['Destination']['time']

    return ' '.join([dep, "->", arr, ": "])


def journeyString(trip):
    journey = []
    for part in trip:
        partStr = [
            part['Origin']['name'], "(",
            part['name'], ", ",
            part['Origin'].get('track', ''), ")"]
        journey.append(''.join(partStr))

    journey.append(part['Destination']['name'])
    return ' - '.join(journey)


def checkStatus(status):
    if status != 200:
        sys.exit("Request not completed!")


def getCoordinates():
    location.start_updates()
    for i in range(20):
        loc = location.get_location()
        accuracy = loc['horizontal_accuracy']
        if accuracy < 50:
            break
        time.sleep(0.1)
    location.stop_updates()
    
    if accuracy > 50:
        print("CAREFUL! Accuracy (%.0f m) might be low!" % (accuracy))

    lat = int(GPSFACTOR * loc['latitude'])
    lon = int(GPSFACTOR * loc['longitude'])

    return lat, lon


def printDuration(tripInfo):
    print(OUTPUTWIDTH*"-")
    print(durationString(tripInfo))


def printTrip(tripInfo):
    journey = journeyString(tripInfo)
    print(*textwrap.wrap(journey, OUTPUTWIDTH), sep='\n')
    print()


def homeWork(origin, dest, time):
    rString = requestStringTime(origin, dest, time)
    r       = requests.get(baseUrl + rString)

    checkStatus(r.status_code)

    trips = r.json()['TripList']['Trip']

    for trip in trips:
        tripInfo = trip['Leg']
        printDuration(tripInfo)
        printTrip(tripInfo)


def anywhereToHome(time):
#    lat = int(55.656 * GPSFACTOR)
#    lon = int(12.633 * GPSFACTOR)

    lat, lon = getCoordinates()

    rString = requestStringHome(lon, lat, home1, time)
    r       = requests.get(baseUrl + rString)

    checkStatus(r.status_code)

    trips = r.json()['TripList']['Trip']

    for trip in trips:
        tripInfo = trip['Leg']
        printDuration(tripInfo)
        printTrip(tripInfo)


def main():
    now  = datetime.datetime.now()
    time = now.time()
    day  = now.weekday()

    timeEarly = (time > datetime.time(8)) and (time < datetime.time(9, 30))
    timeLate  = (time > datetime.time(16)) and (time < datetime.time(17, 30))
    dayCheck  = day in list(range(5))

#    timeEarly = True
#    timeLate = True
#    timeLate = False

    if dayCheck and timeEarly:
        homeWork(home1, work1, time)
    elif dayCheck and timeLate:
        homeWork(work1, home1, time)
    else:
        anywhereToHome(time)


if __name__ == "__main__":
    main()


