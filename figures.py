

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
# a lot of these need to be worked on and organized. That is likely to be a future project for you guys.


def bar4MovementDayNight(dfBar, ax, width = 4):
    """
    Creates DayNight movement bar to go along with actigram and other behavioral figures.

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
    """

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and 'InterpulseInterval'
    :param dfxTicks: Xtick dataframe, initialized in DataFrameCreationMethods
    :param show_title: True if title is desired, False otherwise. Default is True.
    :param show_xLabels: True if x labels are desired, False otherwise. Default is True.
    :param show_average: True if average line is desired, False otherwise. Default is True. Average line gets worse the shorter the video is.
    :return: axes object filled with IPI figure.
    """

    # takes pulses where Interpulse interval is not null
    df = dfComplex[dfComplex.InterpulseInterval.notnull() & (dfComplex.InterpulseInterval < 30)]

    # renames axes object for convenience
    ax = axis

    # global frame taken from complex dataframe
    x = df['global frame']

    # interpulse interval taken from dataframe
    y = df['InterpulseInterval']

    # plotting method
    ax.plot(x, y, c = '#7f7f7f', lw = 2, label= 'IPI')

    # averaging method
    if show_average:
        ym = y.rolling(window=250).mean()

        ax.plot(x, ym, c = 'b', lw = 2, label= 'average')

        ax.set_xlabel(xlabel=r'Zeitgeber Time')
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
        justXticks = dfxTicks[dfxTicks.TickType == 'hour_absolute']

        xTicks = justXticks['xTicks'].tolist()
        xTickLabels = justXticks['xTickLabels'].tolist()

        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels)

    else:
        ax.get_xaxis().set_visible(False)

    if show_title: ax.set_title(jelly_title + '- Interpulse Interval')

def initiatiorsHistogramFigure(jelly_title, ax, dfComplex, vertical = True, show_title = True, show_degreeLabels = True):
    """
    Shows a normalized histogram of usage across the degrees of a jellyfish. Each entry represents the total pulses of
    that particular degree on the jellyfish as a percent of total pulses.

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param ax: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Only uses the 'bounded angle'
    :param vertical:    if vertical is true, the plot is plotted vertically, with the degree locations on the y axis.
                        if vertical is false, the plot is plotted horizontally, with the degree locations on the x axis.
    :param show_title:  True if title is desired, False otherwise. Default is True.
    :param show_degreeLabels:  True if labels (x or y ticks depending on orientation) are desired, False otherwise. Default is True.
    :return: axes object filled with IPI figure.
    """

    # aggregates angle measurements from 'bounded angle' column
    #
    dfGrouped = dfComplex.groupby(['bounded angle'])['bounded angle'].agg('count')


    degrees = dfGrouped.index.tolist()
    counts = dfGrouped.tolist()
    numPulses = sum(counts)

    # normalizes the amount into precent of pulses
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


def initiatiorsHistogramQueryFigure(jelly_title, ax, dfComplex, question, vertical=True, show_title=True, show_degreeLabels = True):
    """
    you can query the complex dataframe data to look at differences in subsets of data. Filtered Complex DF is an input
    for the 'initiatiorsHistogramFigure' method.

    useful questions:
        'DayOrNight == \'Night\''   # queries all the night pulses
        'DayOrNight == \'Day\''     # queries all the day pulses


    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param ax: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Only uses the 'bounded angle'
    :param question: Query to filter the complex dataframe. questions are written as pandas query functions.
    :param vertical:    if vertical is true, the plot is plotted vertically, with the degree locations on the y axis.
                        if vertical is false, the plot is plotted horizontally, with the degree locations on the x axis.
    :param show_title:  True if title is desired, False otherwise. Default is True.
    :param show_degreeLabels:  True if labels (x or y ticks depending on orientation) are desired, False otherwise. Default is True.
    :return: axes object filled with IPI figure.
    """

    dfQuery = dfComplex.query(question)

    initiatiorsHistogramFigure(jelly_title, ax, dfQuery, vertical, show_title, show_degreeLabels)


def ysensitivity(dataframe, metric):
    """
    DO NOT WORRY ABOUT THIS ONE. Represents grouping metrics. I need to comment a bit more on it and maybe rework it.

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
    """
    Given a dataframe to plot, this also plots error bars on either size with binning and error bars.

    :param dfY:
    :param x:
    :param ax:
    :param windowSize:
    :return:
    """

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


def sensitivityCCFigure(jelly_title, axis, dfComplex, dfxTicks, show_title = True, show_xLabels = True, show_Legend = True):
    """
    Plots the different sensativities of the center changed figure. S10, S20, S30 are all plotted together.
    Does not seem to be working rn?
    TODO: fix sensitivityCCFigure.

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and all of the CenterChangedS** columns.
    :param dfxTicks: Xtick dataframe, initialized in DataFrameCreationMethods
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



    x = ysensitivity(df, 'CenterChangedAfterS10')['min time'].tolist()

    x = list(range(len(x)))


    yA1S1 = ysensitivity(df, 'CenterChangedAfterS10')['count'].rolling(window=windowSize).mean()

    yA1S2 = ysensitivity(df, 'CenterChangedAfterS20')['count'].rolling(window=windowSize).mean()

    yA1S3 = ysensitivity(df, 'CenterChangedAfterS30')['count'].rolling(window=windowSize).mean()

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

    if show_title: ax.set_title(jelly_title + ' Jellyfish Centers Changed sensitivity Testing')


# In[39]:


def centersChangedFigure(jelly_title, axis, dfComplex, dfxTicks, show_title = True, show_xLabels = True, show_Legend = True, sensitivity = 30, bounds = (0,0.8), figType = 'Long'):
    """
    Creates the "Interpulse Change" figure. This figure tracks the amount of pulses that change from one location to 
    another. This is done by aggregating the True/False "CentersChangedS__' columns. 
    Very similar to the sensativities figure although it only

    "centers" describes the angle of a pulse, specifically the bounded angle. If the bounded angle of the next pulse is
    within the sensitivity distance.
    
    TODO: refactor the columns involved to say "AngleChangedS10"
    TODO: change this so it is the inverse, and a measure of centralization, not decentralization


    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and all of the CenterChangedS** columns.
    :param dfxTicks: Xtick dataframe, initialized in DataFrameCreationMethods
    :param show_title:
    :param show_xLabels:
    :param show_Legend:
    :param sensitivity: Specified sensitivity. Can be either 10, 20, or 30, corresponding to the 3 CentersChanged Columns
    :param bounds: Y axis bounds of the figure. The amount of center's changed is bounded between 0 and 1 because it
                    is tracking the percentage of centers that changed within a given bin. Therefore these bounds should
                    be between 0 and 1.
    :param figType: Specifies the length of ComplexDF. Desribes what sort of xtick system to use: house, 10mintues, or
                    minutes. This may need to be added to every graph, or be automated for the length of the slice being
                    used.
                    3 options: 'Long', 'Medium', and 'Short'
    :return:
    """


    ax = axis

    # filters the dataframe
    df = dfComplex[dfComplex.AbsoluteMinute.notnull()]

    #BINSIZE is number of minutes to use in each bin
    #WINDOWSIZE is the number of bins to use in the rolling average and standard error analysis
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
        10 : 'CenterChangedAfterS10',
        20 : 'CenterChangedAfterS20',
        30 : 'CenterChangedAfterS30',
    }

    # gets the figure dataframe by binning various items.
    dfFigure = ysensitivity(df, switcher.get(sensitivity))

    # finds a list of x values
    x = list(range(len(dfFigure)))

    # gets just the counts from the figure provided.
    dfY = dfFigure['count']

    # plots the data onto the axes object
    plotBinAverageWithErrorBars(dfY, x, ax, WINDOWSIZE)

    # sets y bounds using input
    ax.axis(ymin = bounds[0], ymax = bounds[1])

    # sets labels
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% pulses IC')

    # sets grid
    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
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

