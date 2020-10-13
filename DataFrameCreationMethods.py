

import os

from pathlib import Path

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import datetime

from datetime import datetime, timedelta

import math

########################################################################################################################
# **** GLOBAL VARIABLES ****

DEBUG = True
CHIME = True

########################################################################################################################

"""Definitions:
center = a site of initiations
centroid = center of the jellyfish

"""
def calculateDistance(c1, c2):
    dist = math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2)
    return dist

def distanceBetween(a1, a2):
    """ Finds the distance between two centers values in number of segements
    if 5 degree data is used there will be 72 segemnets and each segment will
    be 5 degrees. Therefore a distance of 3 segments will be 15 degrees.
    """
    if(a1 == a2):
        return 0
    elif(a1<a2):
        l = a1
        m = a2
    else:
        l = a2
        m = a1
    h = l + 360

    d1 = h - m
    d2 = m - l
    d = min([d1,d2])

    if d < 360:
        return d
    else:
        return "ERROR, fix this function :("


def centerChanged(a1, a2, sensativity):
    """
        Determines if the center has changed between two center values where each center value is an angle.
        Distance between the two centers is calculated using distance().
        If the distance between the two is less than or equal to the
        sensativity interval this indicates the center has not changed and
        thus false is returned.

        Sensativity is the integer value determining whether the center will or not.
    """
    d = distanceBetween(a1, a2)

    if d <= sensativity:
        return False
    else:
        return True


def createComplexDF(angleDataPath, orientationDF, FRAMERATE, STARTDATETIME, DAYLIGHTSAVINGS = False):
    """
    Creates a complex data frame as a CSV and takes in angle and orientation data during a specified time frame.

    # INPUTS (processingScript.py)
    angleDataPath = path to angle data from files -needs to be clarified ***AJ***
    orientationDF = needs to be clarified ***AJ***
    FRAMERATE = frames per second
    STARTDATETIME = specifies start date time
    DAYLIGHTSAVINGS = specifies if during daylight savings or not

    # OUTPUTS
    DF with information on frame, centroid, angle (raw and bounded), time, movement (center changed boolean and distance)
    """
    dfPaths = [dir for dir in sorted(angleDataPath.iterdir()) if dir.name != '.DS_Store']
# what's happening in these simpleDFs
    simpleDFs = []

    for i, dfPath in enumerate(dfPaths):

        tempSimpleData = pd.read_csv(str(dfPath), header=0)

        pathStem = dfPath.stem

        if DEBUG: print('pathStem: {}'.format(pathStem))

        movementSegment = int(pathStem[pathStem.rindex('_')+1:])

        chunkName = pathStem[:pathStem.rindex('_')]

        tempSimpleData['chunk name'] = chunkName
        tempSimpleData['movement segment'] = movementSegment

        simpleDFs.append(tempSimpleData)

    simpleConcatDF = pd.concat(simpleDFs)

    simpleConcatDF = simpleConcatDF.merge(orientationDF, how='left', on='movement segment')

    simpleConcatDF['oriented angle'] = simpleConcatDF['angle'] - simpleConcatDF['orientation factor']

    orientedAngleList = simpleConcatDF['oriented angle'].tolist()

    angleLimits = list(range(360))

    boundAngles = []

    for ang in orientedAngleList:
        if math.isnan(ang):
            boundAngles.append(None)
        else:
            boundAngles.append(angleLimits[int(ang)%360])

    simpleConcatDF['bounded angle'] = boundAngles

    if DEBUG: print(simpleConcatDF.head())

    angles = list(simpleConcatDF['bounded angle'])

    angles1After = angles[1:]
    angles1After.append(np.nan)

    angles2After = angles[2:]
    angles2After.append(np.nan)
    angles2After.append(np.nan)

    angles3After = angles[3:]
    angles3After.append(np.nan)
    angles3After.append(np.nan)
    angles3After.append(np.nan)
# adds columns of angles1, angles2, and angles3 after. Angles after what?
    simpleConcatDF['angles1After'] = angles1After
    simpleConcatDF['angles2After'] = angles2After
    simpleConcatDF['angles3After'] = angles3After

    if DEBUG: print(simpleConcatDF.head())

    simpleConcatArr = simpleConcatDF.to_numpy()
    header = list(simpleConcatDF.columns.values)

    if DEBUG: print("header: {}".format(header))

    angleArrIndex = header.index('bounded angle')
    angles1AfterIndex = header.index('angles1After')

    centroidXindex = header.index('centroid x')
    centroidYindex = header.index('centroid y')
# added additional columns to ComplexDF
    addedDataCols = ['TimeDelta',
                     'AbsoluteMinute',
                     'DateTime',
                     'ZeitgeberTime',
                     'ZeitgeberSec',
                     'ZeitgeberMin',
                     'ZeitgeberHour',
                     'ZeitgeberDay',
                     'DayOrNight',
                     'InterpulseInterval',
                     'CenterChangedAfterS10',
                     'CenterChangedAfterS20',
                     'CenterChangedAfterS30',
                     'distanceMoved',
                     'isHourMark',
                     'isLightChange']

    addedDataFrame = []

    timedelta2Zeitgeber = timedelta(0, 0, 0, 0, 5, 7)

    if DAYLIGHTSAVINGS: timedelta2Zeitgeber = timedelta(0, 0, 0, 0, 5, 8)

    numPulses = len(simpleConcatArr)

    if DEBUG: print(numPulses)

    for i in range(numPulses):
        if i % 1000 == 0: print(i)
        td = timedelta(0, simpleConcatArr[i][0]/FRAMERATE)
        absM = td.days*24*60 + td.seconds//60
        dt = STARTDATETIME + td
        zt = dt - timedelta2Zeitgeber
        ipi = np.nan
        dn = 'Day'
        centroid = (simpleConcatArr[i][centroidXindex], simpleConcatArr[i][centroidYindex])
        a1 = float(simpleConcatArr[i][angleArrIndex])
        a2 = float(simpleConcatArr[i][angles1AfterIndex])
        ccS1 = None
        ccS2 = None
        ccS3 = None
        dm = np.nan
        hourMark = False
        lightChange = 'None'

        if zt.hour >= 12: dn = 'Night'
        elif zt.hour == 11 and zt.minute > 54: dn = 'Night'

        if i < numPulses-1:
            centroidAfter = (simpleConcatArr[i+1][centroidXindex], simpleConcatArr[i+1][centroidYindex])
            ipi = (simpleConcatArr[i+1][0] - simpleConcatArr[i][0])/FRAMERATE
            dm = calculateDistance(centroid, centroidAfter)

        # get last zeithour and see if it's changed
        if i > 0:
            lastHour = addedDataRow[addedDataCols.index('ZeitgeberHour')]
            currHour = zt.hour
            if lastHour != currHour:
                hourMark = True

            lastDN = addedDataRow[addedDataCols.index('DayOrNight')]
            if lastDN != dn:
                if lastDN == 'Day':
                    lightChange = 'toNight'
                else:
                    lightChange = 'toDay'



        if not math.isnan(a1) and not math.isnan(a2):
            ccS1 = centerChanged(a1, a2, 10)
            ccS2 = centerChanged(a1, a2, 20)
            ccS3 = centerChanged(a1, a2, 30)

        # should match added data columns
        addedDataRow = [td, absM, dt, zt, zt.second, zt.minute, zt.hour, zt.day, dn, ipi, ccS1, ccS2, ccS3, dm, hourMark, lightChange]

        addedDataFrame.append(addedDataRow)

    addedDataArr = np.array(addedDataFrame)

    complexDFArr = np.concatenate((simpleConcatArr, addedDataArr), axis=1)

    header.extend(addedDataCols)
    if DEBUG: print(header)

    complexDF = pd.DataFrame(complexDFArr, columns = header)

    if DEBUG: print(complexDF.head())

    return complexDF


def getXtickDF(complexDF):
    """
    Extracts the tick marks, for us in figure plotting.

    # INPUT
    Complex Data Frame
    # OUTPUT
    creates a DF with hour marked data extracted from complexDF
        includes information on when light changed occur
    """
    hour_marks = complexDF[complexDF.isHourMark == True]

    xtickDFheader = ['xTicks', 'xTickLabels', 'TickType']

    globalFrames = hour_marks['global frame'].tolist()
    zeithours = hour_marks['ZeitgeberHour'].tolist()

    tickType = ['hour'] * len(zeithours)

    xticklabels = ['{}:00'.format(i) for i in zeithours]

    light_changes = complexDF[(complexDF.isLightChange == 'toNight') | (complexDF.isLightChange == 'toDay')]

    globalFrames.extend(light_changes['global frame'].tolist())
    xticklabels.extend(light_changes['ZeitgeberHour'].tolist())
    tickType.extend(light_changes.isLightChange.tolist())

    globalFrames.append(complexDF.iloc[0]['global frame'])
    xticklabels.append(complexDF.iloc[0]['ZeitgeberHour'])
    tickType.append('FirstFrame')

    globalFrames.append(complexDF.iloc[-1]['global frame'])
    xticklabels.append(complexDF.iloc[-1]['ZeitgeberHour'])
    tickType.append('LastFrame')

    xtickDF = pd.DataFrame(list(zip(globalFrames, xticklabels, tickType)), columns=xtickDFheader)

    return xtickDF

def createActigramArr(complexDF, FRAMERATE, INTERVAL = 5, pulseExtension = 1/2):
    """
    Reads in complex data as a CSV and takes angle and frame data.
    Creates a CSV with angle + margin set to 1 with all other points set to 0.

    # INPUTS
    Complex Dataframe
    FRAMERATE: frames per second
    INTERVAL: number of points either side of center to set to 1
    pulseExtension: ##### idk :(

    # OUTPUT
    Actigram array...finish this by asking Konnor
    """
    framesPerExtension = int(FRAMERATE*pulseExtension)

    print(complexDF['bounded angle'].unique())


    df = complexDF[complexDF['bounded angle'].notnull()]

    df = df.astype({'bounded angle': 'int64'})

    pulseFrames = df['global frame'].tolist()
    pulseAngles = df['bounded angle'].tolist()

    lastFrame = max(pulseFrames)

    actigramArr = np.zeros((lastFrame+framesPerExtension, 360))

    for i, (frame, angle) in enumerate(zip(pulseFrames, pulseAngles)):
        if DEBUG and i%1000==0:
            print('i: {}, frame: {}, angle: {}'.format(i, frame, angle))

        for extension in range(framesPerExtension):
            for offset in range(-INTERVAL, INTERVAL+1):
                actigramArr[frame+extension][(angle + offset)%360] = 1

    return actigramArr

def createDayNightMovementBar(complexDF, width = 4, movementColor = [255, 0, 0], dayColor = [255, 255, 0], nightColor = [0,0,127]):
"""
Creates a movement bar indicating movement during the daytime or nightime
Movement Color: Red
Day Color: Yellow
Night Color: Navy Blue
"""
    pulseFrames = complexDF['global frame'].tolist()
    pulseMoving = complexDF['bounded angle'].tolist()
    pulseDayNight = complexDF['DayOrNight'].tolist()

    lastFrame = max(pulseFrames)

    barArr = np.zeros((lastFrame, width, 3), dtype='int')

    barArr[:,:] = [255,255,255]

    numPulses = len(pulseFrames)

    for i in range(numPulses-1):

        currPulseFrame = pulseFrames[i]
        nextPulseFrame = pulseFrames[i + 1]
        isMoving = math.isnan(pulseMoving[i])
        isNight = pulseDayNight[i] == 'Night'

        if DEBUG and i%1000==0:
            print('counter: {}, frame: {}, nextframe: {}, isMoving: {}, is night?: {}'.format(i, currPulseFrame, nextPulseFrame, isMoving, isNight))

        if isMoving:
            barArr[currPulseFrame:nextPulseFrame, 0:int(width/2)] = movementColor
        if isNight:
            barArr[currPulseFrame:nextPulseFrame, int(width/2):width] = nightColor
        else:
            barArr[currPulseFrame:nextPulseFrame, int(width/2):width] = dayColor

    return barArr



def createCompressedActigram(actigramCSV, compression_factor):
    """ask Konnor about compressionFactor ***AJ***
    """
    return actigramCSV[::compression_factor]

def createCompressedMovementDayNightBar(barArr, compression_factor):
    """ask Konnor about compression_factor ***AJ***
    """
    return barArr[::compression_factor]


def dfConcatenator(firstDF, firstDFstarttime, secondDF, secondDFstarttime, framerate = 120):
    """concatenates two dataframes together taking into consideration the offset in frames
    """
    td = secondDFstarttime - firstDFstarttime

    frameOffset = (td.days*24*3600 + td.seconds)*framerate

    secondDFCopy = secondDF.copy()

    secondDFCopy['global frame'] = secondDFCopy['global frame'] + frameOffset

    return pd.concat([firstDF, secondDFCopy])
