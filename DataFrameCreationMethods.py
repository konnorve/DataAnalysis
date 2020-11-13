

import numpy as np

import pandas as pd

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

###############################
##### Utility Functions #######
###############################

def makeOutDir(outputDir, folderName):
    outdir = outputDir / folderName
    if not outdir.exists():
        outdir.mkdir()
    return outdir


def calculateDistance(c1, c2):
    """Distance Formula
    Calculates how far the jellyfish has moved by
    finding the distance between two centroids.
    """
    dist = math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2)
    return dist

def distanceBetween(a1, a2):
    """ 
    Returns the shortest difference in degrees betwene two positive, bounded angles. 
    
    # Don't think the following applies anymore: -KVE
    # Finds the distance between two centers values in number of segements
    # if 5 degree data is used there will be 72 segemnets and each segment will
    # be 5 degrees. Therefore a distance of 3 segments will be 15 degrees.
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
    
    # h == high angle (greater than 360 degrees)
    # m == medium angle (between low and 360)
    # l == low angle (between 0 and medium)
    
    d1 = h - m
    d2 = m - l
    d = min([d1,d2])

    if d < 360:
        return d
    else:
        return "ERROR, fix this function :("

# im so sorry but i swear it's spelled 'sensitivity'?,, idk lmao im tired -deb
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

#########################################################
#########################################################
############      DataFrame Creation         ############
#########################################################
#########################################################


def createComplexDF(angleDataPath, orientationDF, FRAMERATE, STARTDATETIME, DAYLIGHTSAVINGS = False):
    """
    Creates a complex data frame as a CSV and takes in angle and orientation data during a specified time frame.

    # INPUTS (processingScript.py)
    angleDataPath = path to angle data from files
    orientationDF = takes in data from an orientation DF
    FRAMERATE = frames per second of recording
    STARTDATETIME = specifies start date time
    DAYLIGHTSAVINGS = specifies if during daylight savings or not

    # OUTPUTS
    DF with information on frame, centroid, angle (raw and bounded), time, movement (center changed boolean and distance)
    """

    # initiate angle data dataframe from directory
    dfPaths = [dir for dir in sorted(angleDataPath.iterdir()) if dir.name != '.DS_Store']

    # simple DFs aka raw angle data are put together into a list and concatenated 

    simpleDFs = []
    # segment angleData in to chunks based on naming conventions? ***clarify AJ***
    for i, dfPath in enumerate(dfPaths):

        # use pandas to read csv 
        tempSimpleData = pd.read_csv(str(dfPath), header=0)
        
        # reads in the name of the angle data
        pathStem = dfPath.stem

        if DEBUG: print('pathStem: {}'.format(pathStem))
        
        # determines the movement segment of the data
        movementSegment = int(pathStem[pathStem.rindex('_')+1:])

        # determines the name of the Chunk
        chunkName = pathStem[:pathStem.rindex('_')]

        #assigns columns equal to the chunk name and movement segment to the dataframe
        tempSimpleData['chunk name'] = chunkName
        tempSimpleData['movement segment'] = movementSegment

        # adds the angle data + its chunk name and movement segment to a list of similar dataframes to be concatenated
        simpleDFs.append(tempSimpleData)

    # concats all the dataframes into one pandas df
    simpleConcatDF = pd.concat(simpleDFs)

    print(simpleConcatDF['chunk name'].iloc[0])
    
    # adds the orientation data from the orientationDF to the simpleConcatDF
    simpleConcatDF = simpleConcatDF.merge(orientationDF, how='left', left_on=['movement segment', 'chunk name'], right_on=['movement segment', 'chunk name'])


    # creates column in simple simpleConcatDF with properly oriented angles of jellyfish by adding angle and orientation factor from orientation segments
    simpleConcatDF['oriented angle'] = simpleConcatDF['angle'] - simpleConcatDF['orientation factor']

    # turns the column of angle data into a python list
    orientedAngleList = simpleConcatDF['oriented angle'].tolist()

    # defines the limits of an angle from [zero to 360 degrees) -kve
    # angle range from 0 to 360 degrees
    angleLimits = list(range(360))

    # turns the orientated angles into integer angle measurements within angleLimits
    boundAngles = []

    # bounded angle is valid integer value angle that and the site on initiation
    for ang in orientedAngleList:
        if math.isnan(ang):
            boundAngles.append(None)
        else:
            boundAngles.append(angleLimits[int(ang)%360])
    # kve:
    # creates column 'bounded angle' which is the modulo of angle by 360 (final oriented angle)
    # bounded angle is most important for data analysis. It maps each pulse on the normal jelly axis. 

    # creates column 'bounded angle' which is the modulo of angle by 360 (final oriented angle)
    simpleConcatDF['bounded angle'] = boundAngles
    # ^^^^^^^MOST IMPORTANT COLUMN^^^^^^^
    
    # indicates the properly oriented angle at which contraction occured
    if DEBUG: print(simpleConcatDF.head())
    
    #turns bounded angles back into a python list
    angles = list(simpleConcatDF['bounded angle'])


    ###################################
    ###### Additional Angle Data ######      
    ###################################
    
    # creates list of angles 1 after current angle. Useful for short pattern recognition. Shifts list by 1 entry. 
    # angles1 after is the first angle after an angle the angle column
    # angles2 after is the second angle after an angle in the angle column
    # angles3 after is the third angle after an angle in the angle column

    # The purpose of creating 3 different angle columns is to easily inspect how much the 
    # jellyfish is (rotating?) within a short time frame -deb -- not really, we just want to see what the next position of initiation is and if the site has changed from previous. -kve

    angles1After = angles[1:]
    angles1After.append(np.nan)

    # creates list of angles 2 after current angle. Useful for short pattern recognition. Shifts list by 2 entries. 
    angles2After = angles[2:]
    angles2After.append(np.nan)
    angles2After.append(np.nan)

    # creates list of angles 3 after current angle. Useful for short pattern recognition. Shifts list by 3 entries. 
    angles3After = angles[3:]
    angles3After.append(np.nan)
    angles3After.append(np.nan)
    angles3After.append(np.nan)

    # adds columns of angles1, angles2, and angles3 after
    simpleConcatDF['angles1After'] = angles1After
    simpleConcatDF['angles2After'] = angles2After
    simpleConcatDF['angles3After'] = angles3After

    if DEBUG: print(simpleConcatDF.head())

    # convert simpleConcatDF from DataFrame array to NumPy array
    simpleConcatArr = simpleConcatDF.to_numpy()
    header = list(simpleConcatDF.columns.values)

    if DEBUG: print("header: {}".format(header))
    
    # finds the index of important columns because numpy does not have String indexing, everything must be indexed to specific numeric indicides in the array
    angleArrIndex = header.index('bounded angle')
    angles1AfterIndex = header.index('angles1After')
    
    centroidXindex = header.index('centroid x')
    centroidYindex = header.index('centroid y')

    #############################
    ######## Time Data #########
    #############################

    

    # added additional columns to ComplexDF specifying time, center changes, and movement

    # added additional columns to ComplexDF specifying time, center changes, and movement
    # TimeDelta = time elapsed in seconds, normalized by the frame rate (??)- deb     
    # AbsoluteMinute = converts the delta time into minutes 
    # DateTime = takes into account when the recording started and adds changes in time
    # ZeitgeberTime = Zeitgeber Time associated with DateTime
    # ZeitgeberSec = Zeitgeber Second associated with DateTime
    # ZeitgeberMin = Zeitgeber Minute associated with DateTime
    # ZeitgeberHour = Zeitgeber Hour associated with DateTime
    # ZeitgeberDay = Zeitgeber Day associated with DateTime
    # DayOrNight = determines if it is Day or Night
    # InterpulseInterval = the time between pulses in seconds
    # CenterChangedAfterS10 = determines if center has changed after sensitivity = 10
    # CenterChangedAfterS20 = determines if center has changed after sensitivity = 20
    # CenterChangedAfterS30 = determines if center has changed after sensitivity = 30
    # distanceMoved = distance between 2 centroids between pulses 
    # isHourMark = determines if there is an XTick or not
    # isLightChange = determines the switch between day and night


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
                     'isLightChange',
                     'by eye verification']
    # initiate a new empty DataFrame for time data
    addedDataFrame = []

    # Zeitgeber time (ZT): A standardized 24-hour notation of the phase in an entrained circadian cycle in which ZT 0 indicates 
    # the beginning of day, or the light phase, and ZT 12 is the beginning of night, or the dark phase.   
    
    # timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=5, hours=7)
    # Zeitgeber time is offset by 7 hours and 5 minutes (ahead or behind?) check if this is actually true though
    # This is determined by when the lights turn on at 7:05 am (pls fact check idk) -deb
    
    timedelta2Zeitgeber = timedelta(0, 0, 0, 0, 5, 7)

    # if daylight savings, Zeitgeber time is offset by 8 hours and 5 minutes
    if DAYLIGHTSAVINGS: timedelta2Zeitgeber = timedelta(0, 0, 0, 0, 5, 8)
    
    # Length of the NumPy array is the number of pulses by the jellyfish (i think? is it just how long the columns are) -deb
    numPulses = len(simpleConcatArr)

    if DEBUG: print(numPulses)

    # () corresponds to the column the variable is associated with 
    
    # td = (TimeDelta) 
    # absM = (AbsoluteMinute)
    # dt = (DateTime) 
    # zt = (ZeitgeberTime) 
    # ipi = (Interpulse Interval) 
    # dn = (Day or Night) 
    # centroid = X,Y coordinates of the jellyfish centroid
    # a1 = angle 1
    # a2 = angle 2
    # ccS1 = (CenterChangedAfterS1) 
    # ccS2 = (CenterChangedAfterS20) 
    # ccS3 = (CenterChangedAfterS30) 
    # dm = (distancedMoved) 
    # hourMark = (isHourMark) 
    # lightChange = (isLightChange)
    
    # Konnor's comments on Deborah's notes:
    # td = time delta, a time delta object that represents the time elapsed from the start of the recording. HH:MM:SS.sss format? 
    #       time delta is calculated using frame of pulse, divided by framerate to get raw seconds, which is then used by timedelta to calculate the rest. 
    # absM = absolute minute. Takes the minute of each pulse. Useful for binning purposes. 
    # dt = date time, datetime object of the exact date and time a pulse takes place. 
    # zt = zeitgeber time. Datetime object. Shift of dt by the time the lights turn on which is ~7am normally and ~8am during daylight savings time
    # ipi = interpulse interval
    # dn = day/night. Specifies 'day' if pulse occured during circadium day (zt time is < 12) and 'night' if pulse occurs during circadium night (zt time is >12, < 24)
    # centroid = (X,Y) position of the jellyfish in pixels, in the tank. 
    # a1 = angle 1 -- angle of the current pulse
    # a2 = angle 2 -- angle of the pulse 1 after the current pulse
    # ccS1, ccS2m, ccS3 = determines if center has changed, True or False. 
    #       True if angle of the pulse after is outside the sensativity distance. 
    #       False if the angle of the pulse after is inside the sensativity distance
    #       Sensativities are 10, 20, and 30 degrees. 
    #       False at S==10 degrees means the next pulse lies within 10 degrees to either side of the current pulse.
    ### ^^^ we should change these to AngleChanged and give actual sensativity (therefore: acS10, acS20, acS30... etc.) Centers is depricated.  
    # dm = distance moved. distance between 2 centroids in pixels
    # hourMark = determines if there is a change in hour to determine if that frame location should be used as an XTick or not.
    # lightChange = determines the switch between day and night. Useful in marking Day/Night changes on bar graph and xtickDf
    
    # initializing various components to create fully complex dataframe
    for i in range(numPulses):
        if i % 1000 == 0: print(i)
        td = timedelta(0, simpleConcatArr[i][0]/FRAMERATE)
        absM = td.days*24*60 + td.seconds//60
        dt = STARTDATETIME + td
        zt = dt - timedelta2Zeitgeber
        ipi = np.nan
        dn = 'Day'  # initalized as Day. All night pulses are then changed to night. 
        centroid = (simpleConcatArr[i][centroidXindex], simpleConcatArr[i][centroidYindex])
        a1 = float(simpleConcatArr[i][angleArrIndex])
        a2 = float(simpleConcatArr[i][angles1AfterIndex])
        ccS1 = None
        ccS2 = None
        ccS3 = None
        dm = np.nan
        hourMark = False
        lightChange = 'None'
        
        # determine if it is day or night in zeitgeber hours
        if zt.hour >= 12: dn = 'Night'
        elif zt.hour == 11 and zt.minute > 54: dn = 'Night'

        # finds distance moved if there is a centroid position in the pulse after. -kve
        # calculates the interpulse interval and the distance moved between pulses
        if i < numPulses-1:
            centroidAfter = (simpleConcatArr[i+1][centroidXindex], simpleConcatArr[i+1][centroidYindex])
            ipi = (simpleConcatArr[i+1][0] - simpleConcatArr[i][0])/FRAMERATE
            dm = calculateDistance(centroid, centroidAfter)
        
        # just checks that the previous pulse exists for comparison
        if i > 0:
            # get last zeithour and see if it's changed
            lastHour = addedDataRow[addedDataCols.index('ZeitgeberHour')]
            currHour = zt.hour
            # if the last hour is not the current hour, than there is an hour mark. that pulse represents the xtick should be a xtick
            if lastHour != currHour:
                hourMark = True
            # specifies a light to dark transition for the xtick df 
            lastDN = addedDataRow[addedDataCols.index('DayOrNight')]
            if lastDN != dn:
                if lastDN == 'Day':
                    lightChange = 'toNight'
                else:
                    lightChange = 'toDay'
        
       # centerChanged(angle1, angle2, sensitivity)
       # if distance between the two angles is less than the sensitivity then
       # center can be treated as unchanged.
       # various sensitivites are offered depending on sensativity of experiment and of videoProcessing program. 
        if not math.isnan(a1) and not math.isnan(a2):
            ccS1 = centerChanged(a1, a2, 10)
            ccS2 = centerChanged(a1, a2, 20)
            ccS3 = centerChanged(a1, a2, 30)

        # should match added data columns
        addedDataRow = [td, absM, dt, zt, zt.second, zt.minute, zt.hour, zt.day, dn, ipi, ccS1, ccS2, ccS3, dm, hourMark, lightChange, np.nan]

        addedDataFrame.append(addedDataRow)
        
    # turns the python list of lists data that was created in the for loop into a numpy array
    addedDataArr = np.array(addedDataFrame)

    # concatenates the simplified numpy dataarr from before and the added dataframe array created from the for loop. 
    complexDFArr = np.concatenate((simpleConcatArr, addedDataArr), axis=1)

    # extends the header to include the added rows
    header.extend(addedDataCols)
    if DEBUG: print(header)

    # pieces together the entire complex datframe, complete with all data and the header
    complexDF = pd.DataFrame(complexDFArr, columns = header)

    if DEBUG: print(complexDF.head())
    
    #returns a pandas dataframe
    return complexDF

###################################
###################################
########## Figure Data ############
###################################
###################################

def createActigramArr(complexDF, FRAMERATE, INTERVAL = 5, pulseExtension = 1/2):
    """
    Reads in complex data as a CSV and takes angle and frame data.
    Creates a Numpy Arr m by n, m = number of frames in recording and n = number of degrees
    Pulses are set to 1, all other space is set to 0 (this makes the actigram image)
    Pulses are represented by a block of black (1) pixels
    Pulse angle and frame number are identified.
    Block is built by INTERVAL pixels on either side of pulse
    Block is extended by pulseExtension (seconds)

    INPUTS
    Complex Dataframe
    FRAMERATE: frames per second
    INTERVAL: number of points either side of center to set to 1

    pulseExtension: seconds to represent the pulse by. pulseExtension * frames gives a framecount which is used to extend the "tick mark" that represents each pulse.

    OUTPUT
    Actigram array which is used in plotting the actigram using imshow.
    Pulseas are 1's and non-pulse pixels are 0.
    pulseExtension: the number of frames used to visualize ticks

    """
    framesPerExtension = int(FRAMERATE*pulseExtension)

    print(complexDF['bounded angle'].unique())

    # gets a dataframe of bounded angles that are not null

    df = complexDF[complexDF['bounded angle'].notnull()]
    
    # converts the bounded angles into ints
    df = df.astype({'bounded angle': 'int64'})
    
    # changes the frame and angles to python lists
    pulseFrames = df['global frame'].tolist()
    pulseAngles = df['bounded angle'].tolist()

    startFrame = min(pulseFrames)
    lastFrame = max(pulseFrames)
    
    # creates the image array of zeros. m x n (m == all frames of recording, n == degrees on the jellyfish)
    actigramArr = np.zeros((lastFrame+framesPerExtension-startFrame, 360))

    # enumerates through pulses. gets the frame and angle from each pulse coming from the complex dataframe and changes the necessary pixels from 0 to 1. 
    for i, (frame, angle) in enumerate(zip(pulseFrames, pulseAngles)):
        if DEBUG and i%1000==0:
            print('i: {}, frame: {}, angle: {}'.format(i, frame, angle))
        
        for extension in range(framesPerExtension):
            # offset the pulse + and - INTERVAL (ex: for INTERVAL = 5, width would be 11, (5+1+5) 
            for offset in range(-INTERVAL, INTERVAL+1):
                actigramArr[frame-startFrame+extension][(angle + offset)%360] = 1

    return actigramArr


def dfConcatenator(firstDF, firstDFstarttime, secondDF, secondDFstarttime, framerate = 120):
    """
#   concatenates two dataframes together taking into consideration the offset in frames
    """
    td = secondDFstarttime - firstDFstarttime

    frameOffset = (td.days*24*3600 + td.seconds)*framerate

    secondDFCopy = secondDF.copy()

    secondDFCopy['global frame'] = secondDFCopy['global frame'] + frameOffset

    return pd.concat([firstDF, secondDFCopy])


