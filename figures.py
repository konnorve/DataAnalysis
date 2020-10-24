

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import math
from scipy import stats
import DataFrameCreationMethods as cdf

# def readCSV2pandasDF(CSVpath):
#     return pd.read_csv(str(CSVpath), index_col=0)

####### Key things to know #######
# Axis refers to the axes object, not the x or y axis. Every figure must be added in
# similarly, all of the titles, x/y ticks, and visibility methods are from the axes class, not pyplt.


def bar4MovementDayNight(dfBar, ax, width = 4):
    """
    Creates daynight movement bar to go along with actigram and other behavioral figures.

    :param dfBar: Bar dataframe, created in DataFrameCreationMethods. Image array specifying what is
    :param ax: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param width: width of the bar. specified in the creation of the bar.
    :return: axes object filled with bar image.
    """

    dfBar = cdf.createCompressedMovementDayNightBar(dfBar, 10)

    # imshow == Image show. Shows the np array as an image.
    # np.transpose flips the array from verical to horizonal. It goes from being n frames long to n frames wide
    ax.imshow(np.transpose(dfBar, (1, 0, 2)), origin='lower', aspect='auto')


    ax.set_yticks([width/4, width*3/4])
    ax.set_yticklabels(['Movement', 'Light or Dark'])

    ax.get_xaxis().set_visible(False)

def actigramFigure(dfActigram, dfxTicks, axis, title, rhopaliaPositions360 = [], rhopaliaLabels = [], colormap = cm.seismic):
    """

    :param dfActigram:  np actigram array. n frames long by 360 degrees wide. Must be transposed in order to be made into horizontal image.
                        often these are huge images. Plots that utilize this figure take a while to compile.
                        1's represent pulses, 0's represent non-pulse areas
    :param dfxTicks: Xtick dataframe, initialized in DataFrameCreationMethods
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param title: desired title of the plot.
    :param rhopaliaPositions360: Python list of rhopalia positions
    :param rhopaliaLabels: Python list of corresponding rhopalia labels
    :param colormap: corresponding matplotlib colormap chosen to plot the data.
    :return: axes object filled with actigram image.
    """

    # takes slice of actigram to compress the image to be manageable for our purposes. Otherwise image is thousands of megabytes.
    # takes every 10th row of the actigram to create a sliced image.
    dfActigramComp = cdf.createCompressedActigram(dfActigram, 10)
    dfxTicksComp = dfxTicks.copy()
    # compresses the xticks by a comprable amount
    dfxTicksComp['xTicks'] = dfxTicksComp['xTicks'] / 10

    ax1 = axis

    #imshow function
    ax1.imshow(dfActigramComp.T, origin='lower', aspect='auto', cmap=colormap, interpolation='bilinear')

    #setting y ticks, both axis
    rp360 = rhopaliaPositions360
    rl = rhopaliaLabels

    # if rhopalia are added, then it changes the tick axes so that the rhopalia show up on the left and degress are on the right.
    if len(rhopaliaPositions360) == 0:
        degreeTicks = np.linspace(0, 360, 7)
        degreeLabels = [0, 60, 120, 180, 240, 300, 360]

        ax1.set_yticks(degreeTicks)
        ax1.set_yticklabels(degreeLabels)

        ax1.set_xlabel(xlabel=r'Zeitgeber Time (Hours)')
        ax1.set_ylabel(ylabel='Degrees')

    else:
        ax1.set_yticks(rp360)
        ax1.set_yticklabels(rl)

        ax2 = ax1.twinx()

        degreeTicks = np.linspace(0, 1, 7)
        degreeLabels = [0,60,120,180,240,300,360]

        ax2.set_yticks(degreeTicks)
        ax2.set_yticklabels(degreeLabels)

        # axis labels, both y's and x
        ax1.set_xlabel(xlabel=r'Zeitgeber Time (Hours)')
        ax1.set_ylabel(ylabel='Rhopalia Number and Position')
        ax2.set_ylabel(ylabel='Degrees')

        ax2.grid(False)

    # grids. Changes colors so that grids show regardless of colormap.
    if colormap == cm.binary:
        ax1.grid(which='major', color='#bebeff', linestyle=':', linewidth=1)
    elif colormap == cm.seismic:
        ax1.grid(which='major', color='w', linestyle=':', linewidth=1)
    else:
        ax1.grid(which='major', color='#7f7f7f', linestyle=':', linewidth=1)

    #setting x ticks
    justXticks = dfxTicksComp[dfxTicksComp.TickType == 'hour_relative']

    xTicks = justXticks['xTicks'].tolist()
    xTickLabels = justXticks['xTickLabels'].tolist()

    ax1.set_xticks(xTicks)
    ax1.set_xticklabels(xTickLabels)

    #graph title
    ax1.set_title(title)

    # #AV Lines
    # zNightTrans = dfxTicks.query('ZeitTransition == \'Night\'')['xTicks'].tolist()
    # zDayTrans = dfxTicks.query('ZeitTransition == \'Day\'')['xTicks'].tolist()
    #
    # for i in zDayTrans:
    #     ax1.axvline(x=i, color='yellow', linestyle='--')
    #
    # for i in zNightTrans:
    #     ax1.axvline(x=i, color='blue', linestyle='--')

#
#
## Metrics

def interpulseIntervalFigure(jelly_title, axis, dfComplex, dfxTicks, show_title = True, show_xLabels = True, show_average = True):
    df = dfComplex[dfComplex.InterpulseInterval.notnull() & (dfComplex.InterpulseInterval < 30)]
    ax = axis

    x = df['global frame']

    y = df['InterpulseInterval']

    ax.plot(x, y, c = '#7f7f7f', lw = 2, label= 'IPI')

    if show_average:
        ym = y.rolling(window=250).mean()

        ax.plot(x, ym, c = 'b', lw = 2, label= 'average')

        ax.set_xlabel(xlabel=r'Zeitgeber Time')
        ax.set_ylabel(ylabel='IPI (s)')

    ax.grid(which = 'both', axis = 'y', alpha=0.5, linestyle='--')

    ax.semilogy()

    ax.margins(x=0)

    ax.set_ylim(0.5, 3)

    if show_xLabels:

        justXticks = dfxTicks[dfxTicks.TickType == 'hour_absolute']

        xTicks = justXticks['xTicks'].tolist()
        xTickLabels = justXticks['xTickLabels'].tolist()

        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels)

    else:
        ax.get_xaxis().set_visible(False)

    if show_title: ax.set_title(jelly_title + '- Interpulse Interval')

def initiatiorsHistogramFigure(jelly_title, ax, dfComplex, vertical = True, show_title = True, show_degreeLabels = True):

    dfGrouped = dfComplex.groupby(['bounded angle'])['bounded angle'].agg('count')

    degrees = dfGrouped.index.tolist()
    counts = dfGrouped.tolist()
    numPulses = sum(counts)
    percents = [i/numPulses for i in counts]

    if vertical:
        ax.barh(degrees, percents)

        ax.set_xlabel(xlabel=r'% of total counts')

        ax.margins(y=0)

        if show_degreeLabels:
            ax.set_ylabel(ylabel='Degree')
        else:
            ax.get_yaxis().set_visible(False)
    else:
        ax.bar(degrees, percents)

        ax.set_ylabel(ylabel=r'% of total counts')

        ax.margins(x=0)

        if show_degreeLabels:
            ax.set_xlabel(xlabel='Degree')
        else:
            ax.get_xaxis().set_visible(False)

    if show_title: ax.set_title(jelly_title)

def initiatiorsHistogramQueryFigure(jelly_title, ax, dfComplex, question, vertical = True, show_title = True, show_degreeLabels = True):
    #questions are written as pandas query functions
    #useful questions:
        #'DayOrNight == \'Night\''
        #'DayOrNight == \'Day\''

    dfQuery = dfComplex.query(question)

    initiatiorsHistogramFigure(jelly_title, ax, dfQuery, vertical, show_title, show_degreeLabels)


def ysensativity(dataframe, metric):
    """
    DO NOT WORRY ABOUT THIS ONE

    :param dataframe:
    :param metric:
    :return:
    """

    #subsets dataframe into the only things I need
    dfSubset = dataframe[['binCount', metric,'ZeitgeberTime']]

    #gets a ataframe with the count of items in each bin
    dfBinCounts = dataframe.groupby(['binCount']).count()[['counter']]

    #groups the subset by metric and bin count while applying aggregations
    dfGrouped = dfSubset.groupby(['binCount', metric]).agg(['count','min','max'])
    dfGrouped = dfGrouped.rename(columns={"min": "min time", "max": "max time"})
    dfGrouped.columns = dfGrouped.columns.get_level_values(1)
    dfGrouped['count'] = dfGrouped['count']/dfBinCounts['counter']
    dfFigure = dfGrouped.query( metric + ' == True')
    dfFigure.index = dfFigure.index.get_level_values(0)

    return dfFigure

def plotBinAverageWithErrorBars(dfY, x, ax, windowSize):

    fillColor = 'b'
    fillShade = 0.1

    ym = dfY.rolling(window=windowSize).mean()
    ysd = dfY.rolling(window=windowSize).std()
    yse = np.divide(ysd, math.sqrt(windowSize))
    ya = np.add(ym, yse)
    yb = np.subtract(ym, yse)

    ax.plot(x, ym, c = 'k', lw = 2, label= 'Metric');
    ax.plot(x, ya, c = 'b', lw = 0.5, label='Standard Error Above Average');
    ax.plot(x, yb, c = 'b', lw = 0.5, label='Standard Error Below Average');

    ax.fill_between(x = x, y1 = ya, y2 = yb, color = fillColor, alpha = fillShade)


def sensativityCCFigure(jelly_title, axis, dfComplex, dfxTicks, show_title = True, show_xLabels = True, show_Legend = True):
    """
    DO NOT WORRY ABOUT THIS ONE

    :param jelly_title:
    :param axis:
    :param dfComplex:
    :param dfxTicks:
    :param show_title:
    :param show_xLabels:
    :param show_Legend:
    :return:
    """


    ax = axis

    df = dfComplex[dfComplex.AbsoluteMinute.notnull()]

    #BINSIZE is number of minutes to use in each bin
    BINSIZE = 5
    colorDN = 'b'
    colorND = '#fcd12a'
    windowSize = 20

    #establishes column to groupby and use bins
    df['binCount'] = df['AbsoluteMinute']/BINSIZE
    df['counter'] = 1

    binCount = []
    for item in df['binCount']:
        binCount.append(int(item))

    df['binCount'] = binCount



    x = ysensativity(df, 'CenterChangedAfterS10')['min time'].tolist()

    x = list(range(len(x)))


    yA1S1 = ysensativity(df, 'CenterChangedAfterS10')['count'].rolling(window=windowSize).mean()

    yA1S2 = ysensativity(df, 'CenterChangedAfterS20')['count'].rolling(window=windowSize).mean()

    yA1S3 = ysensativity(df, 'CenterChangedAfterS30')['count'].rolling(window=windowSize).mean()

    print(len(x))
    print(len(yA1S1))
    print(len(yA1S2))
    print(len(yA1S3))

    ax.plot(x, yA1S1, c = 'b', lw = 2, label= 'level of change 1 center after, s = 1');
    ax.plot(x, yA1S2, c = 'g', lw = 2, label= 'level of change 1 center after, s = 2');
    ax.plot(x, yA1S3, c = 'r', lw = 2, label= 'level of change 1 center after, s = 3');


    ax.axis(ymin = 0, ymax = 1)

    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% pulses IC')

    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    if show_xLabels:
        lastx = x[-1]

        compressionFactor = dfxTicks[dfxTicks.TickType == 'hour_absolute'].iloc[0, 0] / lastx

        justXticks = dfxTicks[dfxTicks.TickType == 'hour_absolute']

        justXticks['xTicks'] = justXticks['xTicks'] / compressionFactor

        xTicks = justXticks['xTicks'].tolist()
        xTickLabels = justXticks['xTickLabels'].tolist()

        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels)
    else:
        ax.get_xaxis().set_visible(False)
    if show_Legend: ax.legend()

    if show_title: ax.set_title(jelly_title + ' Jellyfish Centers Changed Sensativity Testing')


# In[39]:


def centersChangedFigure(jelly_title, axis, dfComplex, dfxTicks, show_title = True, show_xLabels = True, show_Legend = True, sensativity = 3, bounds = (0,0.8), figType = 'Long'):

    ax = axis

    df = dfComplex[dfComplex.AbsoluteMinute.notnull()]



    #BINSIZE is number of minutes to use in each bin
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

    binCount = []
    for item in df['binCount']:
        binCount.append(int(item))

    df['binCount'] = binCount

    switcher = {
        1 : 'CenterChangedAfterS10',
        2 : 'CenterChangedAfterS20',
        3 : 'CenterChangedAfterS30',
    }

    dfFigure = ysensativity(df, switcher.get(sensativity))

    x = list(range(len(dfFigure)))

    dfY = dfFigure['count']

    plotBinAverageWithErrorBars(dfY, x, ax, WINDOWSIZE)

    ax.axis(ymin = bounds[0], ymax = bounds[1])

    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% pulses IC')

    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    if show_xLabels:
        lastx = x[-1]

        lastFrame = dfComplex.iloc[-1]['global frame']
        #lastFrame = dfxTicks[dfxTicks.TickType == 'LastFrame'].iloc[0, 0]

        compressionFactor = lastFrame / lastx

        justXticks = dfxTicks[dfxTicks.TickType == 'hour_absolute']

        justXticks['xTicks'] = justXticks['xTicks'] / compressionFactor

        xTicks = justXticks['xTicks'].tolist()
        xTickLabels = justXticks['xTickLabels'].tolist()

        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels)

    else:
        ax.get_xaxis().set_visible(False)

    if show_Legend: ax.legend()

    if show_title: ax.set_title(jelly_title + ' Interpulse Change')

