
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
        Determines if the center has changed between two center values
        Distance between the two centers is calculated using distance()
        If the distance between the two is less than or equal to the
        sensativity interval this indicates the center has not changed and
        thus false is returned.
    """
    d = distanceBetween(a1, a2)

    if d <= sensativity:
        return False
    else:
        return True



def createComplexDF(angleDataPath, orientationDF, FRAMERATE, STARTDATETIME, DAYLIGHTSAVINGS = False):

    dfPaths = [dir for dir in sorted(angleDataPath.iterdir()) if dir.name != '.DS_Store']

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
                     'CenterChangedAfterS1',
                     'CenterChangedAfterS2',
                     'CenterChangedAfterS3',
                     'distanceMoved',
                     'isHourMark']

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


        if not math.isnan(a1) and not math.isnan(a2):
            ccS1 = centerChanged(a1, a2, 10)
            ccS2 = centerChanged(a1, a2, 20)
            ccS3 = centerChanged(a1, a2, 30)

        # should match added data columns
        addedDataRow = [td, absM, dt, zt, zt.second, zt.minute, zt.hour, zt.day, dn, ipi, ccS1, ccS2, ccS3, dm, hourMark]

        addedDataFrame.append(addedDataRow)

    addedDataArr = np.array(addedDataFrame)

    complexDFArr = np.concatenate((simpleConcatArr, addedDataArr), axis=1)

    header.extend(addedDataCols)
    if DEBUG: print(header)

    complexDF = pd.DataFrame(complexDFArr, columns = header)

    if DEBUG: print(complexDF.head())

    return complexDF



def getXtickDF(complexDF):

    hour_marks = complexDF[complexDF.isHourMark == True]

    xtickDFheader = ['xTicks', 'xTickLabels', 'ZeitTransition']

    globalFrames = hour_marks['global frame'].tolist()
    zeithours = hour_marks['ZeitgeberHour'].tolist()

    zeitTransition = []
    for i in range(len(zeithours)):
        zt = None
        if zeithours[i] == 12:
            zt = 'Night'
        if zeithours[i] == 0:
            zt = 'Day'
        zeitTransition.append(zt)

    xticklabels = []
    for i in range(len(zeithours)):
        xticklabels.append(str(zeithours[i]) + ":00")

    xtickDF = pd.DataFrame(list(zip(globalFrames, xticklabels, zeitTransition)), columns=xtickDFheader)

    return xtickDF


# Reads in complex data as a CSV and takes angle and frame data.
# Creates a CSV with angle + margin set to 1 with all other points set to 0.
#
# INPUT: Complex Dataframe.
# OUTPUT: CSV has no header.

# INTERVAL is number of points either side of center to set to 1
def createActigramArr(complexDF, FRAMERATE, INTERVAL = 5, pulseExtension = 1/2):
    framesPerExtension = int(FRAMERATE*pulseExtension)

    print(complexDF['bounded angle'].unique())


    df = complexDF[complexDF['bounded angle'].notnull()]

    df = df.astype({'bounded angle': 'int64'})

    pulseFrames = df['global frame'].tolist()
    pulseAngles = df['bounded angle'].tolist()

    lastFrame = pulseFrames[-1]

    actigramArr = np.zeros((lastFrame+framesPerExtension, 360))

    counter = 0
    for frame, angle in zip(pulseFrames, pulseAngles):
        if DEBUG:
            print('counter: {}, frame: {}, angle: {}'.format(counter, frame, angle))
            counter += 1

        for extension in range(framesPerExtension):
            for offset in range(-INTERVAL, INTERVAL+1):
                actigramArr[frame+extension][(angle + offset)%360] = 1

    return actigramArr

def createCompressedActigram(actigramCSV, compression_factor):
    return actigramCSV[::compression_factor]

def createCompressedXtickDFF(xtickDF, compression_factor):
    xtickDF['xTicks'] = xtickDF['xTicks']/compression_factor
    return xtickDF