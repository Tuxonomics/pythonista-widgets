#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 1 19:32:32 2018

@author: Jonas K

WORK IN PROGRESS

A small sript to use Rejseplanen's public REST API. The output needs to fit
into Pythonista's terminal (40 characters on iPhone).
"""

import requests
import sys
import datetime
import textwrap
from conf import baseUrl, home1, work1

import location


OUTPUTWIDTH = 40


def requestStringOffset(origin, dest, timeOffset = 0):
    trip = [
        "/trip?originId=", str(origin),
        "&destId=", str(dest),
        "&offsetTime=", str(timeOffset),
        "&format=json"]
    return ''.join(trip)


def requestStringTime(origin, dest, time):
    trip = [
        "/trip?originId=", str(origin),
        "&destId=", str(dest),
        "&time=", str(time),
        "&format=json"]
    return ''.join(trip)


def durationString(trip):
    duration = ' '.join(
        [trip[0]['Origin']['time'],
         "->", trip[-1]['Destination']['time'], ": "])
    return duration


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


def printDuration(tripInfo):
    print(OUTPUTWIDTH*"-")
    print(durationString(tripInfo))


def printTrip(tripInfo):
    journey = journeyString(tripInfo)
    print(*textwrap.wrap(journey, OUTPUTWIDTH), sep='\n')
    print()


def toWork(time):
    twTrip  = requestStringTime(home1, work1, time)
    r       = requests.get(baseUrl + twTrip)

    checkStatus(r.status_code)

    trips = r.json()['TripList']['Trip']

    for trip in trips:
        tripInfo = trip['Leg']
        printDuration(tripInfo)
        printTrip(tripInfo)


def toHome():
    print("home")
    #TODO: get home based on GPS

    location.start_updates()
    loc = location.get_location()
    location.stop_updates()

    lat = loc['latitude']
    lon = loc['longitude']



    print('latitude', lat, 'longitude', lon)


def main():
    now  = datetime.datetime.now()
    time = now.time()
    day  = now.weekday()

    timeCheck = (time > datetime.time(8)) and (time < datetime.time(9, 30))
    dayCheck  = day in list(range(5))

    timeCheck = True

    if dayCheck and timeCheck:
        toWork(time)
    else:
        toHome()


if __name__ == "__main__":
    main()


