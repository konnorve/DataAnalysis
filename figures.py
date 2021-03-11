

import matplotlib.patches as mpatches
import math
from datetime import timedelta as td
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
from datetime import datetime
####### Key things to know #######
# Axis refers to the axes object, not the x or y axis. Every figure must be added in
# similarly, all of the titles, x/y ticks, and visibility methods are from the axes class, not pyplt.
# a lot of these need to be worked on and organized. That is likely to be a future project for you guys.

###  Definitions
# bar4MovementDayNight- the skinny bar with the yellow/blue day/night, and the red ticks for movement // (plotBar)
# actigramFigure- the blue graph with time vs degrees // (SeismicActigram)
# interpulseInterval- the spikey grey one with the blue line going through the middle // (InterpulseInterval)
# initiatiorsHistogramFigure- blue histogram // (CenterHistogramHorizonatal/Vertical)
# initiatiorsHistogramQueryFigure- (centersHistogramDayANDNightPlot)
# ysensitivity- IGNORE FOR NOW
# plotBinAverageWithErrorBars- not used in plottingMethods?
# sensitivityCCFigure- commented out rn/not working :(
# centersChangedFigure- 'highlight' blue line with black line down the middle // (CenterChanged)


## matplotlib.axes (common attributes used)
# imshow  // Display data as an image
# set_xticks //	Set the xaxis' tick locations
# set_xticklabels //	Set the xaxis' labels with list of string labels.
# set_yticks	// Set the yaxis' tick locations.
# set_yticklabels  // Set the yaxis' labels with list of string labels.

###################################
###################################
######## Accessory Methods ########
###################################
###################################

def dt2int(dt):
    """
    turns datetime object into int
    """
    return int(datetime.timestamp(dt))


def createDayNightMovementBar(complexDF, width, pulseExtension=8, movementColor = [255, 128, 0], dayColor = [255, 255, 0], nightColor = [85,85,85]):
    """
    Creates a movement bar indicating movement during the daytime or nightime
    Movement Color: Red
    Day Color: Yellow
    Night Color: Navy Blue
    """
    df = complexDF.copy()

    df['ZeitgeberTime'] = df['ZeitgeberTime'].apply(lambda dt: dt2int(dt))

    pulseTimes = df['ZeitgeberTime'].tolist()
    pulseMoving = complexDF['bounded angle'].tolist()
    pulseDayNight = complexDF['DayOrNight'].tolist()

    startTime = min(pulseTimes)
    lastTime = max(pulseTimes)
    actigramLen = lastTime - startTime + pulseExtension

    barArr = np.zeros((actigramLen, width, 3), dtype='int')

    start_datetime = complexDF.ZeitgeberTime.min().replace(microsecond=0)

    barArr[:,:] = [255,255,255]

    numPulses = len(pulseTimes)

    for i in range(actigramLen):
        if (start_datetime + td(seconds=i)).hour in range(12,24):
            barArr[i, int(width / 2):width] = nightColor
        else:
            barArr[i, int(width / 2):width] = dayColor

    for i in range(numPulses-1):

        currPulseTime = pulseTimes[i] - startTime
        nextPulseTime = pulseTimes[i+1] - startTime
        isMoving = math.isnan(pulseMoving[i])

        if isMoving:
            barArr[currPulseTime:nextPulseTime, 0:int(width/2)] = movementColor

    return barArr



def chooseFigType(complexDF):
    start_datetime = complexDF.ZeitgeberTime.min()
    end_datetime = complexDF.ZeitgeberTime.max()

    timeperiod_length = end_datetime - start_datetime

    long_td = td(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=4, weeks=0)
    short_td = td(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=25, hours=0, weeks=0)

    if timeperiod_length > long_td:
        return 'Long'
    elif timeperiod_length < short_td:
        return 'Short'
    else:
        return 'Medium'


def applyXticks(complexDF, ax):
    # designed to fix the issues in the last plotting method, make them not reliant on ticking
    # from dataframe, only on start and end time points
    # turn off ticks on first axis
    ax.get_xaxis().set_visible(False)

    # create a new axis to tick on
    tickAx = ax.twiny()

    # move that twin axis from top of plot to bottom of plot
    tickAx.get_xaxis().set_ticks_position('bottom')

    start_datetime = complexDF.ZeitgeberTime.min()
    end_datetime = complexDF.ZeitgeberTime.max()

    num_seconds = (start_datetime - end_datetime).total_seconds()

    figType = chooseFigType(complexDF)

    # print('figType: {}'.format(figType))

    if figType == 'Long':
        tick_start = start_datetime.replace(second=0, minute=0, microsecond=0, hour=start_datetime.hour + 1)
        tick_spacing = td(hours=1)
    elif figType == 'Medium':
        tick_start = start_datetime.replace(second=0, minute=(start_datetime.minute // 10) * 10 + 10, microsecond=0)
        tick_spacing = td(minutes=10)
    elif figType == 'Short':
        tick_start = start_datetime.replace(second=0, minute=start_datetime.minute + 1, microsecond=0)
        tick_spacing = td(minutes=1)

    tick_datetime = tick_start
    tick_datetimes = []
    while True:
        if tick_datetime < end_datetime:
            tick_datetimes.append(tick_datetime)
            tick_datetime += tick_spacing
        else:
            break

    if figType == 'Long':
        xticklabels = [t.hour for t in tick_datetimes]
    else:
        xticklabels = ['{}:{:02}'.format(t.hour, t.minute) for t in tick_datetimes]

    xtickMarks = [(start_datetime - dt).total_seconds() / num_seconds for dt in tick_datetimes]

    tickAx.set_xticks(xtickMarks)
    tickAx.set_xticklabels(xticklabels)


###################################
###################################
############# Figure ##############
###################################
###################################

def bar4MovementDayNight(complexDF, ax, width = 4):
    """
    Creates DayNight movement bar to go along with actigram and other behavioral figures.

    :param dfBar: Bar dataframe, created in DataFrameCreationMethods. Image array specifying what is
    :param ax: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param width: width of the bar. specified in the creation of the bar.
    :return: axes object filled with bar image.
    """
    # takes slice of bar to compress the image to be manageable for our purposes
    # takes every 10th row of the bar to create a sliced image

    dfBar = createDayNightMovementBar(complexDF, width)

    # imshow == Image show. Shows the np array as an image.
    # np.transpose flips the array from vertical to horizontal. It goes from being n frames long to n frames wide
    ax.imshow(np.transpose(dfBar, (1, 0, 2)), origin='lower', aspect='auto', interpolation='none')

    # labels the Day/Night section on the top half and the Movement section on the bottom half of the plotBar
    ax.set_yticks([width/4, width*3/4])
    ax.set_yticklabels(['Movement', 'Light or Dark'])

    # x axis not visible
    ax.get_xaxis().set_visible(False)


def actigramFigure(dfActigram, complexDF, axis, rhopaliaPositions360 = [], rhopaliaLabels = []):
    """
    :param dfActigram:  np actigram array. n frames long by 360 degrees wide. Must be transposed in order to be made into horizontal image.
                        often these are huge images. Plots that utilize this figure take a while to compile.
                        1's represent pulses, 0's represent non-pulse areas
    :param complexDF: complexDf
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param title: desired title of the plot.
    :param rhopaliaPositions360: Python list of rhopalia positions
    :param rhopaliaLabels: Python list of corresponding rhopalia labels
    :param colormap: corresponding matplotlib colormap chosen to plot the data.
    :return: axes object filled with actigram image.
    """

    # parses actigram dataframe
    actigramArr = dfActigram[0]
    legend = dfActigram[1]

    # renames axes object for convenience
    ax1 = axis

    # imshow function - show the sliced actogram; ('.T' flips rows and columns, because it's a transposed array?)
    ax1.imshow(actigramArr.transpose((1,0,2)), origin='lower', aspect='auto', interpolation='bilinear')

    # if statement setting y ticks, both axes
    rp360 = rhopaliaPositions360
    rl = rhopaliaLabels

    # if no rhopalia are added, degrees on the left
    if len(rhopaliaPositions360) == 0:

        # use numpy, space from 0 to 360 degrees, every 60 degrees
        degreeTicks = np.linspace(0, 360, 7)
        # label each tick starting from 0 to 360 degrees, every 60 degrees
        degreeLabels = [0, 60, 120, 180, 240, 300, 360]

        ax1.set_yticks(degreeTicks)
        ax1.set_yticklabels(degreeLabels)

        ax1.set_xlabel(xlabel=r'Zeitgeber Time (Hours)')
        ax1.set_ylabel(ylabel='Degrees')

    # if rhopalia are added, then it changes the tick axes so that the rhopalia show up on the left and degrees are on the right.
    else:
        ax1.set_yticks(rp360)
        ax1.set_yticklabels(rl)  # creates and labels as many yticks as there are rhopalia   x

        # twinx(): create a twin axes sharing the x axis.
        ax2 = ax1.twinx()

        degreeTicks = np.linspace(0, 1, 7) # seven intervals between 0 and 1. why 1 and not 360?   x
        # label each tick starting from 0 to 360 degrees, every 60 degrees
        degreeLabels = [0,60,120,180,240,300,360]

        ax2.set_yticks(degreeTicks)
        ax2.set_yticklabels(degreeLabels)

        # axis labels, both y's and x
        ax1.set_xlabel(xlabel=r'Zeitgeber Time (Hours)')
        ax1.set_ylabel(ylabel='Rhopalia Number and Position')
        ax2.set_ylabel(ylabel='Degrees')

        ax2.grid(False)

    # if actigram is colored, it adds labels
    if bool(legend):
        key_rgb_pairs = [(key, [x / 255 for x in legend[key]]) for key in legend.keys()]
        patches = [mpatches.Patch(color=c, label=l) for l, c in key_rgb_pairs]
        ax1.legend(handles=patches, loc=1, bbox_to_anchor=(1.1, 1), borderaxespad=0.)

    # grids. Changes colors so that grids show regardless of colormap.
    ax1.grid(which='major', color='#bebeff', linestyle=':', linewidth=1)

    #setting x ticks
    applyXticks(complexDF, ax1)


def interpulseInterval(axis, dfComplex, ipi_after = True, show_xLabels = True, show_average = True):
    """
    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and 'InterpulseInterval'
    :param show_title: True if title is desired, False otherwise. Default is True.
    :param show_xLabels: True if x labels are desired, False otherwise. Default is True.
    :param show_average: True if average line is desired, False otherwise. Default is True. Average line gets worse the shorter the video is.
    :return: axes object filled with IPI figure.
    """
    try:
        if ipi_after:
            # takes pulses where Interpulse interval is not null [and is lower than thirty?  x]
            df = dfComplex[dfComplex.InterpulseInterval_After.notnull() & (dfComplex.InterpulseInterval_After < 30)]

            # interpulse interval taken from dataframe for y axis data
            y = df['InterpulseInterval_After']
        else:
            df = dfComplex[dfComplex.InterpulseInterval_before.notnull() & (dfComplex.InterpulseInterval_before < 30)]
            y = df['InterpulseInterval_before']

    except Exception as error:
        # could happen with older dataframes without Ipi_after or ipi_before
        df = dfComplex[dfComplex.InterpulseInterval.notnull() & (dfComplex.InterpulseInterval < 30)]
        y = df['InterpulseInterval']

    # renames axes object for convenience
    ax = axis

    # global frame taken from complex dataframe (line sets x to the dataframe column with that label  x)
    # global frame taken from complex dataframe for x axis data
    x = df['ZeitgeberTime'].apply(lambda dt: dt2int(dt)).to_numpy()


    # plotting method
    ax.plot(x, y, c = '#7f7f7f', lw = 2, label= 'IPI')  # specifying color, linewidth, label text   x

    # averaging method
    # shown as a blue line
    if show_average:
        ym = y.rolling(window=250).mean()  # calculates rolling average in/of groups of 250   x

        ax.plot(x, ym, c = 'b', lw = 2, label= 'average')  # adds to ax a plot of the global dataframe vs rolling avg  x

        ax.set_xlabel(xlabel=r'Zeitgeber Time')  # sets x and y labels
        ax.set_ylabel(ylabel='IPI (s)')

    # adds gridlines. Major and minor ticks. Only y axis. Alpha is the opacity of the lines.
    ax.grid(which = 'both', axis = 'y', alpha=0.5, linestyle='--')

    #changes y axis to log scale
    ax.semilogy()

    # zeros the margins
    ax.margins(x=0)

    #fixed limits. Makes graphs compareable
    ax.set_ylim(0.5, 3)

    # x tick method.
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)

    else:
        ax.get_xaxis().set_visible(False)  # don't bother doing that^ if we're not gonna see it


def pulseRate(axis, dfComplex, pr_after = True, show_xLabels = True, show_average = True):
    """

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and 'PulseRate'
    :param show_title: True if title is desired, False otherwise. Default is True.
    :param show_xLabels: True if x labels are desired, False otherwise. Default is True.
    :param show_average: True if average line is desired, False otherwise. Default is True. Average line gets worse the shorter the video is.
    :return: axes object filled with IPI figure.
    """
    
    try:
        if pr_after:
            # takes pulses where Interpulse interval is not null [and is lower than thirty?  x]
            df = dfComplex[dfComplex.PulseRate_After.notnull() & (dfComplex.PulseRate_After < 30)]

            temp_df = df[['PulseRate_After']]
        else:
            df = dfComplex[dfComplex.PulseRate_Before.notnull() & (dfComplex.PulseRate_Before < 30)]
            temp_df = df[['PulseRate_Before']]

    except Exception as error:
        # could happen with older dataframes without Ipi_after or ipi_before
        df = dfComplex[dfComplex.PulseRate.notnull() & (dfComplex.PulseRate < 30)]
        temp_df = df[['PulseRate']]

    # renames axes object for convenience
    ax = axis

    # global frame taken from complex dataframe (line sets x to the dataframe column with that label  x)
    # global frame taken from complex dataframe for x axis data
    temp_df['xaxis'] = df['ZeitgeberTime'].apply(lambda dt: dt2int(dt)).tolist()
    temp_df = temp_df.set_index('xaxis')
    temp_df = temp_df.sort_index()

    # plotting method
    ax.plot(temp_df, c = '#7f7f7f', lw = 2, label= 'Pulse Rate')  # specifying color, linewidth, label text   x

    # averaging method
    # shown as a blue line
    if show_average:
        ax.plot(temp_df.rolling(window=250).mean(), c = 'b', lw = 2, label= 'average')  # adds to ax a plot of the global dataframe vs rolling avg  x

        ax.set_xlabel(xlabel=r'Zeitgeber Time')  # sets x and y labels
        ax.set_ylabel(ylabel='Pulse Rate (Hz)')

    # adds gridlines. Major and minor ticks. Only y axis. Alpha is the opacity of the lines.
    ax.grid(which = 'both', axis = 'y', alpha=0.5, linestyle='--')

    # zeros the margins
    ax.margins(x=0)

    #fixed limits. Makes graphs compareable
    ax.set_ylim(0, 2)

    # x tick method.
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)

    else:
        ax.get_xaxis().set_visible(False)  # don't bother doing that^ if we're not gonna see it


def distanceMoved(axis, dfComplex, dm_after = True, maxDMthreshold = 50, show_xLabels = True, show_average = True):
    """

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and 'PulseRate'
    :param show_title: True if title is desired, False otherwise. Default is True.
    :param show_xLabels: True if x labels are desired, False otherwise. Default is True.
    :param show_average: True if average line is desired, False otherwise. Default is True. Average line gets worse the shorter the video is.
    :return: axes object filled with IPI figure.
    """

    try:
        if dm_after:
            df = dfComplex[dfComplex.DistanceMoved_After.notnull() & (dfComplex.DistanceMoved_After < maxDMthreshold)]
            y = df['DistanceMoved_After']
        else:
            df = dfComplex[dfComplex.DistanceMoved_Before.notnull() & (dfComplex.DistanceMoved_Before < maxDMthreshold)]
            y = df['DistanceMoved_Before']

    except Exception as error:
        df = dfComplex[dfComplex.distanceMoved.notnull() & (dfComplex.distanceMoved < maxDMthreshold)]
        y = df['distanceMoved']


    # renames axes object for convenience
    ax = axis

    # global frame taken from complex dataframe (line sets x to the dataframe column with that label  x)
    # global frame taken from complex dataframe for x axis data
    x = df['ZeitgeberTime'].apply(lambda dt: dt2int(dt)).to_numpy()

    # plotting method
    ax.plot(x, y, c = '#7f7f7f', lw = 2, label= 'Distance Moved')  # specifying color, linewidth, label text   x

    # averaging method
    # shown as a blue line
    if show_average:
        ym = y.rolling(window=250).mean()  # calculates rolling average in/of groups of 250   x

        ax.plot(x, ym, c = 'b', lw = 2, label= 'average')  # adds to ax a plot of the global dataframe vs rolling avg  x

        ax.set_xlabel(xlabel=r'Zeitgeber Time')  # sets x and y labels
        ax.set_ylabel(ylabel='Distance Moved (px)')

    # adds gridlines. Major and minor ticks. Only y axis. Alpha is the opacity of the lines.
    ax.grid(which = 'both', axis = 'y', alpha=0.5, linestyle='--')

    ax.semilogy()

    # zeros the margins
    ax.margins(x=0)

    # fixed limits. Makes graphs compareable
    ax.set_ylim(0.1, 300)

    #fixed limits. Makes graphs compareable
    # ax.set_ylim(0, 50)

    # x tick method.
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)

    else:
        ax.get_xaxis().set_visible(False)  # don't bother doing that^ if we're not gonna see it


def jelly_trajectory(complexDFslice, fig, ax, image_max_x, image_max_y, a=0.4):
    ax.set_xlim(0, image_max_x)
    ax.set_ylim(0, image_max_y)

    x_arr = complexDFslice['centroid x'].to_numpy()
    y_arr = complexDFslice['centroid y'].to_numpy()
    # converts Zeitgeber time into int (epoch time)
    time_arr = complexDFslice['ZeitgeberTime'].apply(lambda dt: dt2int(dt)).to_numpy()

    # shape all the coordinate points into segments to plot continuous line
    points = np.array([x_arr, y_arr]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(time_arr.min(), time_arr.max())

    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.viridis), ax=ax)

    lc = LineCollection(segments, cmap='viridis', norm=norm, alpha=a)  # change opacity with alpha

    # Set the values used for colormapping
    lc.set_array(time_arr)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    # normalize the color scale to the color map
    cmap = cm.viridis

    # color a portion of the color scale according to the normalized colors we've set
    for i in range(len(time_arr)):
        color = cmap(norm(time_arr[i]))
        ax.plot(x_arr[i], y_arr[i], marker='o', c=color, alpha=a)

    # labelling stuff
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')


def initiatiorsHistogramFigure(ax, dfComplex, rhopos=[], rholab=[], vertical = True, title=None,
                               show_degreeLabels = True, show_just_degree_labels=False,
                               show_just_rhopalia_labels=False, shadeAroundRhopaliaInterval = 10,
                               constraints = [], question=None, delta_sleep_wake=None):
    """
    Shows a normalized histogram of usage across the degrees of a jellyfish. Each entry represents the total pulses of
    that particular degree on the jellyfish as a percent of total pulses.
    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param ax: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Only uses the 'bounded angle' column
    :param vertical:    if vertical is true, the plot is plotted vertically, with the degree locations on the y axis.
                        if vertical is false, the plot is plotted horizontally, with the degree locations on the x axis.
    :param show_title:  True if title is desired, False otherwise. Default is True.
    :param show_degreeLabels:  True if labels (x or y ticks depending on orientation) are desired, False otherwise. Default is True.
    :param question: Query to filter the complex dataframe. questions are written as pandas query functions.
    :return: axes object filled with IPI figure.
    """

    if question:
        dfQuery = dfComplex.query(question)
    else:
        dfQuery = dfComplex

    dfQuery = dfQuery[dfQuery['bounded angle'].notnull()]

    dfQuery['bounded angle'] = dfQuery['bounded angle'].apply(lambda x: int(x))

    degrees = range(360)

    ax1 = ax

    # delta_sleep_wake column (determines +/- sleep vs. Wake)
    if delta_sleep_wake:
        wake_counts = [0]*360
        sleep_counts = [0]*360

        for i, row in dfQuery.iterrows():
            if row['SleepWake_median_ipi_after'] == 'Wake':
                wake_counts[row['bounded angle']] += 1
            else:
                sleep_counts[row['bounded angle']] += 1

        wake_total = sum(wake_counts)
        sleep_total = sum(sleep_counts)

        if wake_total == 0:
            wake_percents = wake_counts
        else:
            wake_percents = [i / wake_total for i in wake_counts]
        if sleep_total == 0:
            sleep_percents = sleep_counts
        else:
            sleep_percents = [i / sleep_total for i in sleep_counts]

        percents = [sp - wp for sp, wp in zip(sleep_percents, wake_percents)]
    else:
        counts = [0]*360

        for i, row in dfQuery.iterrows():
            counts[row['bounded angle']] += 1

        total_pulses = sum(counts)

        if total_pulses == 0:
            percents = counts
        else:
            percents = [i / total_pulses for i in counts]

    rp360 = rhopos
    rl = rholab
    # interesting, this originally makes a horizontal/vertical bar plot;
    # what's the math diff between this and using Hist()?   x [something to do with the normalization?]
    # For CenterHistogramVertical
    if vertical:
        ax1.barh(degrees, percents)

        ax1.set_xlabel(xlabel=r'% of total counts')

        ax1.margins(y=0)

        if len(constraints) != 0:
            ax1.set_xlim(left=constraints[0], right=constraints[1])

        for rp in rhopos:
            ax1.axhline(rp, alpha=0.5, color='gray', lw=1)
            if rp < shadeAroundRhopaliaInterval:
                ax1.axhspan(0, rp + shadeAroundRhopaliaInterval, alpha=0.25, color='gray', lw=0)
                ax1.axhspan(360 - shadeAroundRhopaliaInterval + rp, 360, alpha=0.25, color='gray', lw=0)
            elif rp + shadeAroundRhopaliaInterval > 360:
                ax1.axhspan(rp - shadeAroundRhopaliaInterval, 360, alpha=0.25, color='gray', lw=0)
                ax1.axhspan(0, shadeAroundRhopaliaInterval - 360 + rp, alpha=0.25, color='gray', lw=0)
            else:
                ax1.axhspan(rp - shadeAroundRhopaliaInterval, rp + shadeAroundRhopaliaInterval, alpha=0.25,
                            color='gray', lw=0)

        if show_degreeLabels:
            ax1.set_ylabel(ylabel='Degree')

            ax2 = ax1.twinx()
            ax2.set_yticks([i/360 for i in rp360])
            ax2.set_yticklabels(rl)
            ax2.set_ylabel(ylabel='Rhopalia Label')
        elif show_just_degree_labels:
            ax1.set_ylabel(ylabel='Degree')
        elif show_just_rhopalia_labels:
            ax1.get_yaxis().set_visible(False)
            ax2 = ax1.twinx()
            ax2.set_yticks([i / 360 for i in rp360])
            ax2.set_yticklabels(rl)
            ax2.set_ylabel(ylabel='Rhopalia Label')
        else:
            ax1.get_yaxis().set_visible(False)



    # For CenterHistogramHorizontal
    else:
        ax1.bar(degrees, percents)

        ax1.set_ylabel(ylabel=r'fraction of total counts')

        ax1.margins(x=0)

        if len(constraints) != 0:
            ax1.set_ylim(bottom=constraints[0], top=constraints[1])

        for rp in rhopos:
            ax1.axvline(rp, alpha=0.5, color='gray', lw=1)
            if rp < shadeAroundRhopaliaInterval:
                ax1.axvspan(0, rp + shadeAroundRhopaliaInterval, alpha=0.25, color='gray', lw=0)
                ax1.axvspan(360 - shadeAroundRhopaliaInterval + rp, 360, alpha=0.25, color='gray', lw=0)
            elif rp + shadeAroundRhopaliaInterval > 360:
                ax1.axvspan(rp - shadeAroundRhopaliaInterval, 360, alpha=0.25, color='gray', lw=0)
                ax1.axvspan(0, shadeAroundRhopaliaInterval - 360 + rp, alpha=0.25, color='gray', lw=0)
            else:
                ax1.axvspan(rp - shadeAroundRhopaliaInterval, rp + shadeAroundRhopaliaInterval, alpha=0.25,
                            color='gray', lw=0)

        if show_degreeLabels:
            ax1.set_xlabel(xlabel='Degree')

            ax2 = ax1.twiny()
            ax2.set_xticks([i/360 for i in rp360])
            ax2.set_xticklabels(rl)
            ax2.set_xlabel(xlabel='Rhopalia Label')
        elif show_just_degree_labels:
            ax1.set_xlabel(xlabel='Degree')
        elif show_just_rhopalia_labels:
            ax1.get_xaxis().set_visible(False)
            ax2 = ax1.twiny()
            ax2.set_xticks([i / 360 for i in rp360])
            ax2.set_xticklabels(rl)
            ax2.set_xlabel(xlabel='Rhopalia Label')
        else:
            ax1.get_xaxis().set_visible(False)

    if title is not None: ax1.set_title(title)


def rho_usage(ax, aggSeries, vertical=True, title=None, constraints=[]):
    posSeries= aggSeries > 0

    if vertical:
        ax.barh(aggSeries.index, aggSeries, color=posSeries.map({True: 'b', False: 'r'}))
        ax.set_xlabel(xlabel=r'% of total counts')
        if len(constraints) != 0:
            ax.set_xlim(left=constraints[0], right=constraints[1])
    else:
        ax.bar(aggSeries, color=posSeries.map({True: 'b', False: 'r'}))
        ax.set_ylabel(xlabel=r'% of total counts')
        if len(constraints) != 0:
            ax.set_ylim(bottom=constraints[0], top=constraints[1])

    if title is not None: ax.set_title(title)


def ysensitivity(dataframe, metric):
    """
    DO NOT WORRY ABOUT THIS ONE. Represents grouping metrics. I need to comment a bit more on it and maybe rework it.
    I'm worried.   x
    :param dataframe:
    :param metric:
    :return:
    """

    #subsets dataframe into the only things I need
    dfSubset = dataframe[['binCount', metric,'ZeitgeberTime']]

    #gets a dataframe with the count of items in each bin
    dfBinCounts = dataframe.groupby(['binCount']).count()[['counter']]

    #groups the subset by metric and bin count while applying aggregations
    dfGrouped = dfSubset.groupby(['binCount', metric]).agg(['count','min','max'])
    dfGrouped = dfGrouped.rename(columns={"min": "min time", "max": "max time"})
    dfGrouped.columns = dfGrouped.columns.get_level_values(1)
    dfGrouped['count'] = dfGrouped['count']/dfBinCounts['counter']
    dfFigure = dfGrouped.query( metric + ' == True')
    dfFigure.index = dfFigure.index.get_level_values(0)

    return dfFigure

# ref: binCount comes from the AbsoluteMinute column once divided into bins of 5 mins -see def sensitivityCCFigure   x

def plotBinAverageWithErrorBars(dfY, x, ax, windowSize):
    """
    Given a dataframe to plot, this also plots error bars on either size with binning and error bars.
    Check the centersChangedFigure function to understand dfY, and check below for the other params if I haven't addressed it up here yet   x

    :param dfY:
    :param x:
    :param ax:
    :param windowSize: determines width of the rolling average; set to 20 in sensitivityCCFig, and 20/5/1 in the
    centersChangedFigure function for long, med & short sized figs respectively

    :return:
    """

    fillColor = 'b'
    fillShade = 0.1

    ym = dfY.rolling(window=windowSize).mean()  # rolling average of dfY  x
    ysd = dfY.rolling(window=windowSize).std()  # rolling standard deviation of dfY  x
    yse = np.divide(ysd, math.sqrt(windowSize))  # divides each standard deviation from ysd via dfY by sqrt of rolling avg number?   x
    ya = np.add(ym, yse)  # finds the respective values labeled below  x
    yb = np.subtract(ym, yse)

    ax.plot(x, ym, c = 'k', lw = 2, label= 'Metric');
    ax.plot(x, ya, c = 'b', lw = 0.5, label='Standard Error Above Average');
    ax.plot(x, yb, c = 'b', lw = 0.5, label='Standard Error Below Average');

    ax.fill_between(x = x, y1 = ya, y2 = yb, color = fillColor, alpha = fillShade)

# def centersChangedFigure(axis, dfComplex, show_xLabels = True, show_Legend = True, sensitivity = 30, bounds = (0,0.8), figType = 'Long'):
def centralizationFigure(axis, dfComplex, show_xLabels=True, show_Legend=True,
                             sensitivity=30, bounds=(0, 1)):
    """
    Creates the "Interpulse Change" figure. This figure tracks the amount of pulses that change from one location to
    another. This is done by aggregating the True/False "CentersChangedS__' columns.

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and all of the CenterChangedS** columns.
    :param show_title: presumably left blank because they're all just: "true or false, show this detail?"  x
    :param show_xLabels:
    :param show_Legend:
    :param sensitivity: Specified sensitivity. Can be either 10, 20, or 30, corresponding to the 3 CentersChanged Columns
    :param bounds: Y axis bounds of the figure. The amount of center's changed is bounded between 0 and 1 because it
                    is tracking the percentage of centers that changed within a given bin. Therefore these bounds should
                    be between 0 and 1.
    :param figType: Specifies the length of ComplexDF. Describes what sort of xtick system to use: house, 10minutes, or
                    minutes. This may need to be added to every graph, or be automated for the length of the slice being
                    used.
                    3 options: 'Long': 20 bins of 5 minutes, 'Medium': 5 bins of 1 minute, and 'Short': 1 with 1  x
    :return:
    """


    ax = axis

    # filters the dataframe [to fill 'df' with every cell from AbsoluteMinute with any value present? i think?   x]
    df = dfComplex[dfComplex.AbsoluteMinute.notnull()]

    figType = chooseFigType(dfComplex)

    # BINSIZE is number of minutes to use in each bin
    # WINDOWSIZE is the number of bins to use in the rolling average and standard error analysis
    if figType == 'Long':
        BINSIZE = 5
        WINDOWSIZE = 20
    elif figType == 'Medium':
        BINSIZE = 1
        WINDOWSIZE = 5
    elif figType == 'Short':
        BINSIZE = 1
        WINDOWSIZE = 1


    #establishes column to groupby and use bins
    df['binCount'] = df['AbsoluteMinute']/BINSIZE
    df['counter'] = 1

    # counts the entries in the bins
    binCount = []
    for item in df['binCount']:
        binCount.append(int(item))

    # creates a column that has bin counts
    df['binCount'] = binCount

    switcher = {
        10 : 'InitiatorSameAfterS10',
        20 : 'InitiatorSameAfterS20',
        30 : 'InitiatorSameAfterS30',
    }

    # gets the figure dataframe by binning various items.
    dfFigure = ysensitivity(df, switcher.get(sensitivity))

    # finds a list of x values
    x = list(range(len(dfFigure)))

    # gets just the counts from the figure provided.
    dfY = dfFigure['count']

    # plots the data onto the axes object
    plotBinAverageWithErrorBars(dfY, x, ax, WINDOWSIZE)  # unsure- is this initializing an array or something, or missing a . after plot?   x

    # sets y bounds using input
    ax.axis(ymin = bounds[0], ymax = bounds[1])

    # sets labels
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% centralized')

    # sets grid
    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)
    else:
        ax.get_xaxis().set_visible(False)

    if show_Legend: ax.legend()


def ganglia_centralization(axis, dfComplex, show_xLabels=True, show_Legend=True, bounds=(0, 1)):



    ax = axis

    figType = chooseFigType(dfComplex)

    # BINSIZE is number of minutes to use in each bin
    # WINDOWSIZE is the number of bins to use in the rolling average and standard error analysis
    if figType == 'Long':
        BINSIZE = 'H'
    elif figType == 'Medium':
        BINSIZE = '10T'
    elif figType == 'Short':
        BINSIZE = 'T'

    dfY = createRhoplaiaCentralizationDF(dfComplex, BINSIZE)

    ax.plot(dfY)

    # sets y bounds using input
    ax.axis(ymin=bounds[0], ymax=bounds[1])

    # sets labels
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% centralized')

    # sets grid
    ax.grid(axis='y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)
    else:
        ax.get_xaxis().set_visible(False)

    if show_Legend: ax.legend()



def createRhoplaiaCentralizationDF(complexDF, time_bin):
    """
    creates a dataframe with each pulse representing a row and each rhopalia a column.
    1's are assigned to the presumed initiating rhopalia of each pulse
    pulses are timestamped with Zeigeber Time
    """
    usage_df = pd.get_dummies(complexDF['RhopaliaSameAfter'], prefix='RhoSameAfter')

    usage_df['ZeitgeberTime'] = pd.to_datetime(
        complexDF['ZeitgeberTime'],
        format='%Y-%m-%d %H:%M:%S')

    usage_df = usage_df.set_index('ZeitgeberTime')

    aggDF = usage_df.resample(time_bin).sum()

    aggDF = aggDF.div(usage_df.sum(axis=1).resample(time_bin).sum(), axis=0)

    return aggDF.RhoSameAfter_True


def usage_lines(ax, dfComplex, aggUsageDF, show_xLabels=True, show_Legend=True,
                sensitivity=30, bounds=(0, 1)):
    for column in aggUsageDF.columns:
        ax.plot(aggUsageDF.index, aggUsageDF[column], label=column)

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2)

    # sets y bounds using input
    ax.axis(ymin=bounds[0], ymax=bounds[1])

    # sets labels
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% usage')

    # sets grid
    ax.grid(axis='y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)
    else:
        ax.get_xaxis().set_visible(False)


def sleep_areas(ax, dfComplex, aggUsageDF, show_xLabels=True, show_Legend=True,
                sensitivity=30, bounds=(0, 1)):
    trans_agg = aggUsageDF.transpose()
    trans_agg = trans_agg.sort_index()

    ax.stackplot(trans_agg.columns, trans_agg, labels=trans_agg.index.tolist(), colors=cm.tab20(np.linspace(0, 1, 16)))

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2)

    # sets y bounds using input
    ax.axis(ymin=bounds[0], ymax=bounds[1])

    # sets labels
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% usage')

    # sets grid
    ax.grid(axis='y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)
    else:
        ax.get_xaxis().set_visible(False)

def usage_areas(ax, dfComplex, aggUsageDF, show_xLabels=True, show_Legend=True,
                sensitivity=30, bounds=(0, 1)):
    trans_agg = aggUsageDF.transpose()
    trans_agg["sum"] = trans_agg.sum(axis=1)
    trans_agg = trans_agg.sort_values('sum', ascending=False)

    trans_agg = trans_agg.drop(columns='sum')

    ax.stackplot(trans_agg.columns, trans_agg, labels=trans_agg.index.tolist(), colors=cm.tab20(np.linspace(0, 1, 16)))

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2)

    # sets y bounds using input
    ax.axis(ymin=bounds[0], ymax=bounds[1])

    # sets labels
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% usage')

    # sets grid
    ax.grid(axis='y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)
    else:
        ax.get_xaxis().set_visible(False)



def usage_activity_level(ax, dfComplex, aggUsageDF, activity_thresh, show_xLabels=True,
                         show_Legend=True):
    activityThreshDF = aggUsageDF > activity_thresh

    ax.plot(activityThreshDF.sum(axis=1), label=str(activity_thresh))

    # sets labels
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='active count')

    # sets grid
    ax.grid(axis='y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
    if show_xLabels:
        # setting x ticks
        applyXticks(dfComplex, ax)
    else:
        ax.get_xaxis().set_visible(False)

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2)

