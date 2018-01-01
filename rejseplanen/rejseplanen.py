#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 1 19:32:32 2018

@author: Jonas K

WORK IN PROGRESS

A small sript to use Rejseplanen's public REST API. The output needs to fit
into Pythonista's widget terminal (40 characters on iPhone).
"""

import requests
import sys
import datetime
import textwrap
from conf import baseUrl, home1, work1


def workString(origin, dest, timeOffset = 7):
    trip = [
        "/trip?originId=", str(origin),
        "&destId=", str(dest),
        "&offsetTime=", str(timeOffset),
        "&format=json"]
    return ''.join(trip)


def journeyString(trip):
    times = ' '.join(
        [trip[0]['Origin']['time'],
         "->", trip[-1]['Destination']['time'], ": "])

    journey = []
    for part in trip:
        partStr = [
            part['Origin']['name'], "(",
            part['name'], ", ",
            part['Origin'].get('track', ''), ")"]
        journey.append(''.join(partStr))

    journey.append(part['Destination']['name'])
    journey = '-'.join(journey)

    return ''.join([times, journey])


def checkStatus(status):
    if status != 200:
        sys.exit("Request not completed!")


def printTrip(journey):
#    print("---------------------------------------")
    print(*textwrap.wrap(journey, 40), sep='\n')


def toWork():
    twTrip  = workString(home1, work1)
    r       = requests.get(baseUrl + twTrip)
    checkStatus(r.status_code)

    # extract all trips, TODO: add some selection requirements    
    trips = r.json()['TripList']['Trip']
    # take first trip
    trip1   = trips[0]['Leg']
    journey = journeyString(trip1)
    
    printTrip(journey)


def toHome():
    #TODO: get home based on GPS
    print("home")


def main():
    now  = datetime.datetime.now()
    time = now.time()
    day  = now.weekday()
    
    timeCheck = (time > datetime.time(8)) and (time < datetime.time(9, 30))
    dayCheck  = day in list(range(5))
    
    timeCheck = True
    
    if dayCheck and timeCheck:
        toWork()
    else:
       toHome()


if __name__ == "__main__":
    main()
