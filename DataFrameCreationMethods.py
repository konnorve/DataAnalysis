

import numpy as np

import pandas as pd

from datetime import datetime, timedelta

import math

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

########################################################################################################################
# **** GLOBAL VARIABLES ****

DEBUG = True
CHIME = True

########################################################################################################################

"""
Definitions:
center = a site of initiations
centroid = center of the jellyfish
"""

###############################
##### Utility Functions #######
###############################

def makeOutDir(outputDir, folderName):
    """
    Makes an out directory if there is not one. Returns file path as Path object

    Inputs:
    outputDir - Pathlib directory object that directory will be created within
    folderName - Name of directory to be made/returned
    """
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
    Returns the shortest difference in degrees between two positive, bounded angles.
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

    return d

def getClosestRhopalia(raw_angle, rhopos, rholab):

    closet_rholab = rholab[0]
    shortest_distance = distanceBetween(raw_angle, rhopos[0])

    for i in range(1, len(rhopos)):
        dist = distanceBetween(raw_angle, rhopos[i])
        if dist < shortest_distance:
            closet_rholab = rholab[i]
            shortest_distance = dist

    return closet_rholab


def nearbyAngle(a1, a2, sensitivity):
    """
        Determines if the angles has changed between two initiation angle values .
        Distance between the two angle is calculated using distance().

        If the distance from a1 to a2 is less than the sensitivity then True will be returned because we can assume that
        the they are roughly from the same initiator

        Sensitivity is the integer value determining whether the angle will or not.
    """
    d = distanceBetween(a1, a2)

    if d <= sensitivity:
        return True
    else:
        return False

def convertTo360(a):
    """
    converts and angle a (degrees) into an angle bounded between 360
    """
    while a < 0:
        a += 360
    while a >= 360:
        a -= 360
    return a


def loadComplexDF(path, columns2keep='all', describe=False):
    # read in CSV
    complex_df = pd.read_csv(path)

    # if column list is inputted then use that
    if columns2keep != 'all':
        complex_df = complex_df[columns2keep]

    # convert datetime columns into datetime objects
    complex_df['ZeitgeberTime'] = pd.to_datetime(
        complex_df['ZeitgeberTime'],
        format='%Y-%m-%d %H:%M:%S')
    complex_df['DateTime'] = pd.to_datetime(
        complex_df['DateTime'],
        format='%Y-%m-%d %H:%M:%S')

    col_list = list(complex_df.columns)

    # describe dataframe if requested
    if describe:

        if 'Jellyfish' in col_list:
            print('all jellyfish: {} \n'.format(complex_df['Jellyfish'].unique()))

        meta_df = []

        for column, dtype in zip(complex_df.columns, complex_df.dtypes):
            col_slice = complex_df[column].values

            column_row = [column, dtype, min(col_slice), max(col_slice)]

            meta_df.append(column_row)

        print(pd.DataFrame(meta_df, columns=['column', 'dtype', 'min', 'max']))

    return complex_df


def df_image(df, legend={"<class 'str'>": [0, 0, 150],  # blue
                         "<class 'numpy.int64'>": [150, 0, 0],  # red
                         "<class 'numpy.float64'>": [0, 100, 0],  # green
                         "<class 'float'>": [0, 100, 0],  # green
                         "<class 'bool'>": [200, 100, 0],  # orange
                         "<class 'numpy.bool_'>": [200, 100, 0],  # orange
                         "<class 'pandas._libs.tslibs.timestamps.Timestamp'>": [0, 100, 100],  # teal
                         }):
    dtypes = []

    df_len, df_width = df.shape

    print(df_len, df_width)

    image = np.zeros((df_len, df_width, 3))

    for i in range(df_len):
        if i % 50000 == 0: print(i)
        for j in range(df_width):
            dtype = str(type(df.iloc[i, j]))
            if dtype not in dtypes:
                dtypes.append(dtype)
            image[i, j] = legend[dtype]

    print('dtypes: {}'.format(dtypes))

    return image


def plot_df_image(df, df_image):
    legend = {"String": [0, 0, 150],  # blue
              "Integer": [150, 0, 0],  # red
              "Float": [0, 100, 0],  # green
              "Boolean": [200, 100, 0],  # orange
              "Datetime": [0, 100, 100],  # teal
              }

    df_len, df_width = df.shape

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(df_image, aspect='auto', interpolation='nearest')

    plt.xticks(range(df_width), df.columns, rotation=45, ha='right')

    key_rgb_pairs = [(key, [x / 255 for x in legend[key]]) for key in legend.keys()]
    patches = [mpatches.Patch(color=c, label=l) for l, c in key_rgb_pairs]
    ax.legend(handles=patches, loc=1, bbox_to_anchor=(1.1, 1), borderaxespad=0.)

    plt.show()




#########################################################
#########################################################
############      DataFrame Creation         ############
#########################################################
#########################################################


def createComplexDF(angleDataPath, orientationDF, rhopaliaDF, FRAMERATE, STARTDATETIME, DAYLIGHTSAVINGS = False, median_ipi=None):
    """
    Creates a complex data frame as a CSV and takes in angle and orientation data during a specified time frame.

    # INPUTS (processingScript.py)
    angleDataPath = path to angle data from files
    orientationDF = takes in data from an orientation DF
    FRAMERATE = frames per second of recording
    STARTDATETIME = specifies start date time
    DAYLIGHTSAVINGS = specifies if during daylight savings or not

    # OUTPUTS
    DF with information on frame, centroid, angle (raw and bounded), time, movement (initiator same boolean and distance)
    """

    # initiate angle data dataframe from directory
    dfPaths = [csv for csv in sorted(angleDataPath.iterdir()) if csv.name != '.DS_Store']

    # takes out timestamp in chunk name if present:
    if orientationDF.loc[0, 'chunk name'].find('_ts') != -1:
        orientationDF['chunk name'] = [name[:name.find('_ts')] for name in orientationDF['chunk name'].tolist()]

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
    
    # adds the orientation data from the orientationDF to the simpleConcatDF
    simpleConcatDF = simpleConcatDF.merge(orientationDF, how='left', left_on=['movement segment', 'chunk name'], right_on=['movement segment', 'chunk name'])

    simpleConcatDF = simpleConcatDF.astype({'angle': 'float64'})

    # in order to get an accurate angle measurement, the marker angle must be measured
    # selects the marker rhopalia from the list of rhopalia
    orientationRhopalia = rhopaliaDF.loc[rhopaliaDF['Orientation Rho']=='YES']
    assert len(orientationRhopalia) == 1

    orientationMarkerAngle = orientationRhopalia['Rhopalia Position'].iloc[0]

    # creates column in simple simpleConcatDF with properly oriented angles of jellyfish by adding angle and orientation factor from orientation segments
    simpleConcatDF['oriented angle'] = simpleConcatDF['angle'] - simpleConcatDF['orientation factor'] + orientationMarkerAngle

    # turns the column of angle data into a python list
    orientedAngleList = simpleConcatDF['oriented angle'].tolist()

    # turns the orientated angles into integer angle measurements within angleLimits
    boundAngles = []
    closestRhopalia = []
    rhopos = rhopaliaDF['Rhopalia Position'].tolist()
    rholab = rhopaliaDF['Rhopalia Label'].tolist()

    # bounded angle is valid integer value angle that and the site on initiation
    for ang in orientedAngleList:
        if math.isnan(ang):
            boundAngles.append(None)
            closestRhopalia.append(None)
        else:
            boundAngles.append(convertTo360(ang))
            closestRhopalia.append(getClosestRhopalia(ang, rhopos, rholab))

    # kve:
    # creates column 'bounded angle' which is the modulo of angle by 360 (final oriented angle)
    # bounded angle is most important for data analysis. It maps each pulse on the normal jelly axis. 

    # creates column 'bounded angle' which is the modulo of angle by 360 (final oriented angle)
    simpleConcatDF['bounded angle'] = boundAngles
    # ^^^^^^^MOST IMPORTANT COLUMN^^^^^^^

    # creates column that lists the rhopalia closest to the given angle
    simpleConcatDF['closest rhopalia'] = closestRhopalia

    # indicates the properly oriented angle at which contraction occured
    if DEBUG: print(simpleConcatDF.head())

    ###################################
    ###### Additional Angle Data ######
    ###################################

    # turns bounded angles back into a python list
    angles = list(simpleConcatDF['bounded angle'])

    # creates list of angles 1 after current angle. Useful for short pattern recognition. Shifts list by 1 entry.
    # angles1 after is the first angle after an angle the angle column
    # angles2 after is the second angle after an angle in the angle column
    # angles3 after is the third angle after an angle in the angle column

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

    ###################################
    ###### Additional Angle Data ######
    ###################################

    # turns bounded angles back into a python list
    rhopalia_use = list(simpleConcatDF['closest rhopalia'])

    rho1After = rhopalia_use[1:]
    rho1After.append(np.nan)

    # creates list of rho 2 after current angle. Useful for short pattern recognition. Shifts list by 2 entries.
    rho2After = rhopalia_use[2:]
    rho2After.append(np.nan)
    rho2After.append(np.nan)

    # creates list of rho 3 after current angle. Useful for short pattern recognition. Shifts list by 3 entries.
    rho3After = rhopalia_use[3:]
    rho3After.append(np.nan)
    rho3After.append(np.nan)
    rho3After.append(np.nan)

    # adds columns of rho1, rho2, and rho3 after
    simpleConcatDF['rho1After'] = rho1After
    simpleConcatDF['rho2After'] = rho2After
    simpleConcatDF['rho3After'] = rho3After

    ############################################################

    if DEBUG: print(simpleConcatDF.head())

    # convert simpleConcatDF from DataFrame array to NumPy array
    simpleConcatArr = simpleConcatDF.to_numpy()
    header = list(simpleConcatDF.columns.values)

    if DEBUG: print("header: {}".format(header))
    
    # finds the index of important columns because numpy does not have String indexing, everything must be indexed to specific numeric indicides in the array
    angleArrIndex = header.index('bounded angle')
    angles1AfterIndex = header.index('angles1After')

    rhoArrIndex = header.index('closest rhopalia')
    rho1AfterIndex = header.index('rho1After')

    centroidXindex = header.index('centroid x')
    centroidYindex = header.index('centroid y')

    global_frame_index = header.index('global frame')

    #############################
    ##### Pulse Level Data ######
    #############################

    # addeing additional columns (detailed below) to ComplexDF specifying time, center changes, and movement

    # TimeDelta = time elapsed in seconds, normalized by the frame rate (??)- deb
    # AbsoluteMinute = converts the delta time into minutes
    # DateTime = takes into account when the recording started and adds changes in time
    # ZeitgeberTime = Zeitgeber Time associated with DateTime
    # ZeitgeberSec = Zeitgeber Second associated with DateTime
    # ZeitgeberMin = Zeitgeber Minute associated with DateTime
    # ZeitgeberHour = Zeitgeber Hour associated with DateTime
    # ZeitgeberDay = Zeitgeber Day associated with DateTime
    # DayOrNight = determines if it is Day or Night
    # InterpulseInterval_After = the time between pulses in seconds
    # PulseRate_After = frequency of pulsation (pulse level)
    # InitiatorSameAfterS10 = determines if angle has not changed in the next pulse when sensitivity = 10
    # InitiatorSameAfterS20 = determines if angle has not changed in the next pulse when sensitivity = 20
    # InitiatorSameAfterS30 = determines if angle has not changed in the next pulse when sensitivity = 30
    # DistanceMoved_After = distance between 2 centroids between pulses
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
                     'InterpulseInterval_After',
                     'PulseRate_After',
                     'DistanceMoved_After',
                     'InterpulseInterval_Before',
                     'PulseRate_Before',
                     'DistanceMoved_Before',
                     'InitiatorSameAfterS10',
                     'InitiatorSameAfterS20',
                     'InitiatorSameAfterS30',
                     'RhopaliaSameAfter',
                     'isHourMark',
                     'is10MinuteMark',
                     'isMinuteMark',
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
    # ipi_a = (InterpulseInterval_After)
    # pr_a = PulseRate_After
    # dn = (Day or Night)
    # centroid = X,Y coordinates of the jellyfish centroid
    # a1 = angle 1
    # a2 = angle 2
    # isS1 = (InitiatorSameAfterS10)
    # isS2 = (InitiatorSameAfterS20)
    # isS3 = (InitiatorSameAfterS30)
    # dm_a = (distancedMoved)
    # hourMark = (isHourMark)
    # lightChange = (isLightChange)

    # Konnor's comments on Deborah's notes:
    # td = time delta, a time delta object that represents the time elapsed from the start of the recording. HH:MM:SS.sss format?
    #       time delta is calculated using frame of pulse, divided by framerate to get raw seconds, which is then used by timedelta to calculate the rest.
    # absM = absolute minute. Takes the minute of each pulse. Useful for binning purposes.
    # dt = date time, datetime object of the exact date and time a pulse takes place.
    # zt = zeitgeber time. Datetime object. Shift of dt by the time the lights turn on which is ~7am normally and ~8am during daylight savings time
    # ipi_a = InterpulseInterval_After
    # pr_a = PulseRate_After
    # dn = day/night. Specifies 'day' if pulse occured during circadium day (zt time is < 12) and 'night' if pulse occurs during circadium night (zt time is >12, < 24)
    # centroid = (X,Y) position of the jellyfish in pixels, in the tank.
    # a1 = angle 1 -- angle of the current pulse
    # a2 = angle 2 -- angle of the pulse 1 after the current pulse
    # isS1, ccS2m, isS3 = determines if initator angle has changed, True or False.
    #       True if angle of the pulse after is outside the sensitivity distance.
    #       False if the angle of the pulse after is inside the sensitivity distance
    #       Sensativities are 10, 20, and 30 degrees.
    #       False at S==10 degrees means the next pulse lies within 10 degrees to either side of the current pulse.
    ### ^^^ we should change these to AngleChanged and give actual sensitivity (therefore: acS10, acS20, acS30... etc.) Centers is depricated.
    # dm_a = distance moved. distance between 2 centroids in pixels
    # hourMark = determines if there is a change in hour to determine if that frame location should be used as an XTick or not.
    # lightChange = determines the switch between day and night. Useful in marking Day/Night changes on bar graph and xtickDf

    # initializing various components to create fully complex dataframe
    for i in range(numPulses):
        if i % 1000 == 0 and DEBUG: print(i)
        td = timedelta(0, simpleConcatArr[i][global_frame_index]/FRAMERATE)
        absM = td.days*24*60 + td.seconds//60
        dt = STARTDATETIME + td
        zt = dt - timedelta2Zeitgeber
        ipi_a = np.nan
        pr_a = np.nan
        dm_a = np.nan
        ipi_b = np.nan
        pr_b = np.nan
        dm_b = np.nan
        dn = 'Day'  # initalized as Day. All night pulses are then changed to night. 
        centroid = (simpleConcatArr[i][centroidXindex], simpleConcatArr[i][centroidYindex])
        a1 = float(simpleConcatArr[i][angleArrIndex])
        a2 = float(simpleConcatArr[i][angles1AfterIndex])
        isS1 = None
        isS2 = None
        isS3 = None
        r1 = float(simpleConcatArr[i][rhoArrIndex])
        r2 = float(simpleConcatArr[i][rho1AfterIndex])
        rs = None
        hourMark = False
        minMark10 = False
        minMark = False
        lightChange = 'None'
        
        # determine if it is day or night in zeitgeber hours
        if zt.hour >= 12: dn = 'Night'
        elif zt.hour == 11 and zt.minute > 54: dn = 'Night'

        # finds distance moved if there is a centroid position in the pulse after. -kve
        # calculates the InterpulseInterval_After and the distance moved between current and future pulse
        if i < numPulses-1:
            centroidAfter = (simpleConcatArr[i+1][centroidXindex], simpleConcatArr[i+1][centroidYindex])
            ipi_a = (simpleConcatArr[i+1][0] - simpleConcatArr[i][0])/FRAMERATE
            if ipi_a != 0:
                pr_a = 1/ipi_a
            dm_a = calculateDistance(centroid, centroidAfter)

        # finds distance moved if there is a centroid position in the pulse after. -kve
        # calculates the InterpulseInterval_Before and the distance moved between previous and current pulse
        if i>0:
            centroidBefore = (simpleConcatArr[i - 1][centroidXindex], simpleConcatArr[i - 1][centroidYindex])
            ipi_b = (simpleConcatArr[i - 1][0] - simpleConcatArr[i][0]) / FRAMERATE
            if ipi_b != 0:
                pr_b = 1 / ipi_b
            dm_b = calculateDistance(centroid, centroidBefore)
        
        # just checks that the previous pulse exists for comparison
        if i > 0:
            # get last zeithour and see if it's changed
            lastHour = addedDataRow[addedDataCols.index('ZeitgeberHour')]
            currHour = zt.hour
            lastMinute = addedDataRow[addedDataCols.index('ZeitgeberMin')]
            currMinute = zt.minute

            # if the last hour is not the current hour, than there is an hour mark. that pulse represents the xtick should be a xtick
            if lastHour != currHour:
                hourMark = True

            if lastMinute != currMinute:
                minMark = True
                if currMinute % 10 == 0:
                    minMark10 = True

            # specifies a light to dark transition for the xtick df 
            lastDN = addedDataRow[addedDataCols.index('DayOrNight')]
            if lastDN != dn:
                if lastDN == 'Day':
                    lightChange = 'toNight'
                else:
                    lightChange = 'toDay'
        
       # nearbyAngle(angle1, angle2, sensitivity)
       # if distance between the two angles is less than the sensitivity then
       # center can be treated as unchanged.
       # various sensitivites are offered depending on sensitivity of experiment and of videoProcessing program. 
        if not math.isnan(a1) and not math.isnan(a2):
            isS1 = nearbyAngle(a1, a2, 10)
            isS2 = nearbyAngle(a1, a2, 20)
            isS3 = nearbyAngle(a1, a2, 30)

        if r1 is not None and r2 is not None:
            rs = (r1 == r2)

        # should match added data columns
        addedDataRow = [td, absM, dt, zt, zt.second, zt.minute, zt.hour, zt.day, dn, ipi_a, pr_a, dm_a, ipi_b, pr_b,
                        dm_b, isS1, isS2, isS3, rs, hourMark, minMark10, minMark, lightChange, np.nan]

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

    complexDF = complexDF.astype({'global frame': 'int64'})

    if DEBUG: print(complexDF.head())

    # add sleep columns
    if median_ipi is None:
        median_ipi = np.median(complexDF['InterpulseInterval_After'].to_numpy())

    complexDF['SleepWake_median_ipi_after'] = complexDF['InterpulseInterval_After'] > median_ipi
    complexDF = complexDF.replace({'SleepWake_median_ipi_after': {True: 'Sleep', False: 'Wake'}})

    complexDF['SleepWake_median_ipi_before'] = complexDF['InterpulseInterval_Before'] > median_ipi
    complexDF = complexDF.replace({'SleepWake_median_ipi_before': {True: 'Sleep', False: 'Wake'}})
    
    #returns a pandas dataframe
    return complexDF



###################################
###################################
######## Data Aggregation #########
###################################
###################################


def createUsageDF(complexDF, metric='closest rhopalia', prefix='rho'):
    """
    creates a dataframe with each pulse representing a row and each rhopalia a column.
    1's are assigned to the presumed initiating rhopalia of each pulse
    pulses are timestamped with Zeigeber Time
    """
    if prefix == None:
        usage_df = pd.get_dummies(complexDF[metric])
    else:
        usage_df = pd.get_dummies(complexDF[metric], prefix=prefix)

    usage_df['ZeitgeberTime'] = pd.to_datetime(
        complexDF['ZeitgeberTime'],
        format='%Y-%m-%d %H:%M:%S')

    usage_df = usage_df.set_index('ZeitgeberTime')

    return usage_df


def createAggUsageDF(usageDF, time_bin):
    """
    aggregates the usage dataframe on the specified time bin.

    documentation on resampling options at the timeseries pandas documentation page:
    https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html

    returns dataframe with time bins that have percent usage for each rhopalia

    """

    aggDF = usageDF.resample(time_bin).sum()

    aggDF = aggDF.div(usageDF.sum(axis=1).resample(time_bin).sum(), axis=0)

    return aggDF

def createSleepWakeAggDFs_Unnormalized(complexDF, time_bin = 'D', offset = None):
    usage_df_rho = pd.get_dummies(complexDF['closest rhopalia'], prefix='rho')

    usage_df_rho['SleepWake_median_ipi_after'] = complexDF['SleepWake_median_ipi_after']

    usage_df_rho['ZeitgeberTime'] = pd.to_datetime(
        complexDF['ZeitgeberTime'],
        format='%Y-%m-%d %H:%M:%S')

    usage_df_rho['zt_12h_shift'] = usage_df_rho['ZeitgeberTime'] - timedelta(0, 0, 0, 0, 0, 12)

    usage_df_rho = usage_df_rho.set_index('zt_12h_shift')

    aggDF_sleep_counts = usage_df_rho[usage_df_rho['SleepWake_median_ipi_after'] == 'Sleep'].resample(time_bin, offset=offset).sum()
    aggDF_sleep = aggDF_sleep_counts.div(usage_df_rho.sum(axis=1).resample(time_bin, offset=offset).sum(), axis=0)

    aggDF_wake_counts = usage_df_rho[usage_df_rho['SleepWake_median_ipi_after'] == 'Wake'].resample(time_bin, offset=offset).sum()
    aggDF_wake = aggDF_wake_counts.div(usage_df_rho.sum(axis=1).resample(time_bin, offset=offset).sum(), axis=0)

    diffDF = aggDF_sleep - aggDF_wake

    return aggDF_wake, aggDF_sleep, diffDF


def createSleepWakeAggDFs_Normalized(complexDF, time_bin = 'D', offset = None):
    usage_df_rho = pd.get_dummies(complexDF['closest rhopalia'], prefix='rho')

    usage_df_rho['SleepWake_median_ipi_after'] = complexDF['SleepWake_median_ipi_after']

    usage_df_rho['ZeitgeberTime'] = pd.to_datetime(
        complexDF['ZeitgeberTime'],
        format='%Y-%m-%d %H:%M:%S')

    usage_df_rho['zt_12h_shift'] = usage_df_rho['ZeitgeberTime'] - timedelta(0, 0, 0, 0, 0, 12)

    usage_df_rho = usage_df_rho.set_index('zt_12h_shift')

    aggDF_sleep_counts = usage_df_rho[usage_df_rho['SleepWake_median_ipi_after'] == 'Sleep'].resample(time_bin, offset=offset).sum()
    aggDF_sleep = aggDF_sleep_counts.div(usage_df_rho[usage_df_rho['SleepWake_median_ipi_after'] == 'Sleep'].sum(axis=1).resample(time_bin, offset=offset).sum(), axis=0)

    aggDF_wake_counts = usage_df_rho[usage_df_rho['SleepWake_median_ipi_after'] == 'Wake'].resample(time_bin, offset=offset).sum()
    aggDF_wake = aggDF_wake_counts.div(usage_df_rho[usage_df_rho['SleepWake_median_ipi_after'] == 'Wake'].sum(axis=1).resample(time_bin, offset=offset).sum(), axis=0)

    diffDF = aggDF_sleep - aggDF_wake

    return aggDF_wake, aggDF_sleep, diffDF

###################################
###################################
########## Figure Data ############
###################################
###################################

# depricated method for actigram array creation. Uses 'global frame' instead of timestamps

# def createActigramArr(complexDF, FRAMERATE, INTERVAL = 5, pulseExtension = 5,
#                       backgroundColor = [255, 255, 255],
#                       tickColor = [0, 0, 0],
#                       filter = None,
#                       colors=[[0, 0, 150],  # blue
#                               [150, 0, 0],  # red
#                               [0, 100, 0],  # green
#                               [200, 100, 0],  # orange
#                               [0, 100, 100],  # teal
#                               ]
#                       ):
#     """
#     Reads in complex data as a CSV and takes angle and frame data.
#     Creates a Numpy Arr m by n, m = number of frames in recording and n = number of degrees
#     Pulses are set to 1, all other space is set to 0 (this makes the actigram image)
#     Pulses are represented by a block of black (1) pixels
#     Pulse angle and frame number are identified.
#     Block is built by INTERVAL pixels on either side of pulse
#     Block is extended by pulseExtension (seconds)
#
#     INPUTS
#     Complex Dataframe
#     FRAMERATE: frames per second
#     INTERVAL: number of points either side of initiator angle to set to 1
#
#     pulseExtension: seconds to represent the pulse by. pulseExtension * frames gives a framecount which is used to
#                     extend the "tick mark" that represents each pulse.
#
#     OUTPUT
#     Actigram array which is used in plotting the actigram using imshow.
#     Pulseas are 1's and non-pulse pixels are 0.
#     pulseExtension: the number of frames used to visualize ticks
#
#     """
#
#     compression_factor = 30
#
#     framesPerExtension = int(FRAMERATE*pulseExtension/compression_factor)
#     print(framesPerExtension)
#
#     print('unique bounded angles: {}, len: {}'.format(complexDF['bounded angle'].unique(),
#                                                       len(complexDF['bounded angle'].unique())))
#
#     # gets a dataframe of bounded angles that are not null
#
#     df = complexDF[complexDF['bounded angle'].notnull()]
#
#     # converts the bounded angles into ints
#     df = df.astype({'bounded angle': 'int64'})
#
#     # changes the frame and angles to python lists
#     pulseFrames = df['global frame'].tolist()
#     pulseAngles = df['bounded angle'].tolist()
#
#     startFrame = min(pulseFrames)
#     lastFrame = max(pulseFrames)
#
#     # creates the image array of zeros. m x n (m == all frames of recording, n == degrees on the jellyfish)
#     actigramArr = np.zeros((int((lastFrame+framesPerExtension-startFrame)/compression_factor)+120, 360, 3))
#
#     # print('actigram array shape: {}'.format(actigramArr.shape))
#
#     actigramArr[:, :] = backgroundColor
#
#     uniqueVars = []
#     if filter is not None:
#         uniqueVars = df[filter].unique()
#
#         legend = {}
#
#         for i, var in enumerate(uniqueVars):
#             if var == 'Sleep':
#                 legend[var] = [0, 0, 150]
#             elif var == 'Wake':
#                 legend[var] = [150, 0, 0]
#             else:
#                 legend[var] = colors.pop(0)
#
#         filterColumn = df[filter].tolist()
#
#     else:
#         legend = {}
#
#     startFrame = int(startFrame / compression_factor)
#
#     # enumerates through pulses. gets the frame and angle from each pulse coming from the complex dataframe and
#     # changes the necessary pixels from 0 to 1.
#     for i, (frame, angle) in enumerate(zip(pulseFrames, pulseAngles)):
#         if DEBUG and i%10000==0:
#             print('i: {}, frame: {}, angle: {}'.format(i, frame, angle))
#
#         frame = int(frame/compression_factor)
#
#         if len(uniqueVars) > 0:
#             for extension in range(framesPerExtension):
#                 # offset the pulse + and - INTERVAL (ex: for INTERVAL = 5, width would be 11, (5+1+5)
#                 for offset in range(-INTERVAL, INTERVAL + 1):
#                     actigramArr[frame - startFrame + extension][(angle + offset) % 360] = legend[filterColumn[i]]
#         else:
#             for extension in range(framesPerExtension):
#                 # offset the pulse + and - INTERVAL (ex: for INTERVAL = 5, width would be 11, (5+1+5)
#                 for offset in range(-INTERVAL, INTERVAL+1):
#                     actigramArr[frame- startFrame + extension][(angle + offset)%360] = tickColor
#
#     return actigramArr, legend


def createActigramArr(complexDF, INTERVAL=5, pulseExtension=8,
                      backgroundColor=[255, 255, 255],
                      tickColor=[0, 0, 0],
                      filter=None,
                      colors=[[0, 0, 150],  # blue
                              [150, 0, 0],  # red
                              [0, 100, 0],  # green
                              [200, 100, 0],  # orange
                              [0, 100, 100],  # teal
                              ]
                      ):
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
    INTERVAL: number of points either side of initiator angle to set to 1

    pulseExtension: seconds to represent the pulse by. pulseExtension * frames gives a framecount which is used to
                    extend the "tick mark" that represents each pulse.

    OUTPUT
    Actigram array which is used in plotting the actigram using imshow.
    Pulseas are 1's and non-pulse pixels are 0.
    pulseExtension: the number of frames used to visualize ticks

    """

    def dt2int(dt):
        """
        turns datetime object into int
        """
        return int(datetime.timestamp(dt))

    # gets a dataframe of bounded angles that are not null

    df = complexDF[complexDF['bounded angle'].notnull()]

    df['ZeitgeberTime'] = df['ZeitgeberTime'].apply(lambda dt: dt.replace(microsecond=0))

    # converts the bounded angles into ints
    df = df.astype({'bounded angle': 'int64'})

    df['ZeitgeberTime'] = df['ZeitgeberTime'].apply(lambda x: dt2int(x))

    pulseTimes = df['ZeitgeberTime'].to_numpy()
    pulseAngles = df['bounded angle'].to_numpy()

    startTime = min(pulseTimes)
    lastTime = max(pulseTimes)
    actigramLen = lastTime - startTime + pulseExtension

    actigramArr = np.zeros((actigramLen, 360, 3))

    if DEBUG: print('actigram array shape: {}'.format(actigramArr.shape))

    actigramArr[:, :] = backgroundColor

    uniqueVars = []
    if filter is not None:
        uniqueVars = df[filter].unique()

        legend = {}

        for i, var in enumerate(uniqueVars):
            if var == 'Sleep':
                legend[var] = [0, 0, 150]
            elif var == 'Wake':
                legend[var] = [150, 0, 0]
            else:
                legend[var] = colors.pop(0)

        filterColumn = df[filter].tolist()

    else:
        legend = {}

    # enumerates through pulses. gets the frame and angle from each pulse coming from the complex dataframe and
    # changes the necessary pixels from 0 to 1.
    for i, (time, angle) in enumerate(zip(pulseTimes, pulseAngles)):
        if DEBUG and i % 10000 == 0:
            print('i: {}, frame: {}, angle: {}'.format(i, time, angle))

        if len(uniqueVars) > 0:
            for extension in range(pulseExtension):
                # offset the pulse + and - INTERVAL (ex: for INTERVAL = 5, width would be 11, (5+1+5)
                for offset in range(-INTERVAL, INTERVAL + 1):
                    actigramArr[time - startTime + extension][(angle + offset) % 360] = legend[filterColumn[i]]
        else:
            for extension in range(pulseExtension):
                # offset the pulse + and - INTERVAL (ex: for INTERVAL = 5, width would be 11, (5+1+5)
                for offset in range(-INTERVAL, INTERVAL + 1):
                    actigramArr[time - startTime + extension][(angle + offset) % 360] = tickColor

    if DEBUG: print('Done with Actigram creation')

    return actigramArr, legend


def dfValidator(complexDFpostvalidation, chunks2remove=[]):
    validationDF = complexDFpostvalidation[complexDFpostvalidation['by eye verification'].notnull()]

    validationSubsetDF = validationDF[['chunk name', 'angle', 'by eye verification']]

    chunks4validation = list(validationSubsetDF['chunk name'].unique())

    for chunk in chunks2remove:
        if chunk in chunks4validation: chunks4validation.remove(chunk)

    validationSubsetDF = validationSubsetDF[validationSubsetDF['chunk name'].isin(chunks4validation)]

    def getStd_Dev(validationSubset):
        rawAngles = validationSubset['angle'].tolist()
        byEyeAngles = validationSubset['by eye verification'].tolist()

        diff2byeye = []
        for i in range(len(rawAngles)):
            raw_angle = rawAngles[i]
            byeye_angle = convertTo360(byEyeAngles[i])
            if not (math.isnan(raw_angle) or math.isnan(byeye_angle)):
                diff2byeye.append(distanceBetween(raw_angle, byeye_angle))

        squaredDiffs = np.square(diff2byeye)
        summedDiffs = np.sum(squaredDiffs)
        variance = summedDiffs / len(squaredDiffs)
        sd = np.sqrt(variance)

        return sd

    std_dev = getStd_Dev(validationSubsetDF)

    std_dev_bychunk = np.array(list(zip(chunks4validation,
                                        [getStd_Dev(validationSubsetDF[validationSubsetDF['chunk name'] == x]) for x in
                                         chunks4validation])))

    return std_dev, std_dev_bychunk

#
# Depricated method. Used when plotting replied on global frame count and therefore they needed to be synced.
#
# def dfConcatenator(firstDF, firstDFstarttime, secondDF, secondDFstarttime, framerate = 120):
#     """
# #   concatenates two dataframes together taking into consideration the offset in frames
#     """
#     td = secondDFstarttime - firstDFstarttime
#
#     frameOffset = (td.days*24*3600 + td.seconds)*framerate
#
#     secondDFCopy = secondDF.copy()
#
#     secondDFCopy['global frame'] = secondDFCopy['global frame'] + frameOffset
#
#     return pd.concat([firstDF, secondDFCopy])
#
#
