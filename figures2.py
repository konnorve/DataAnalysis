

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import math
from scipy import stats


def actigramFigure(dfActigram, dfxTicks, axis, title, rhopaliaPositions360 = [], rhopaliaLabels = [], colormap = cm.seismic):

    ax1 = axis

    #imshow function
    ax1.imshow(dfActigram.T, origin='lower', aspect='auto', cmap=colormap, interpolation='bilinear')

    #setting y ticks, both axis
    rp360 = rhopaliaPositions360
    rl = rhopaliaLabels

    if len(rhopaliaPositions360) == 0:
        degreeTicks = np.linspace(0, 360, 7)
        degreeLabels = [0, 60, 120, 180, 240, 300, 360]

        ax1.set_yticks(degreeTicks)
        ax1.set_yticklabels(degreeLabels)

        # grids
        ax1.grid(which='major', color='w', linestyle=':', linewidth=1)

    else:
        ax1.set_yticks(rp360)
        ax1.set_yticklabels(rl)

        ax2 = ax1.twinx()

        degreeTicks = np.linspace(0, 1, 7)
        degreeLabels = [0,60,120,180,240,300,360]

        ax2.set_yticks(degreeTicks)
        ax2.set_yticklabels(degreeLabels)

        # axis labels, both y's and x
        ax1.set_xlabel('Time, Zeitgeber (Hours)')
        ax1.set_ylabel('Rhopalia Number and Position')
        ax2.set_ylabel('Degrees')

        # grids
        ax1.grid(which='major', color='w', linestyle=':', linewidth=1)
        ax2.grid(False)

    #setting x ticks
    xTicks = dfxTicks['xTicks'].tolist()
    xTickLabels = dfxTicks['xTickLabels'].tolist()

    ax1.set_xticks(xTicks)
    ax1.set_xticklabels(xTickLabels)


    #graph title
    ax1.set_title(title)

    #AV Lines
    zNightTrans = dfxTicks.query('ZeitTransition == \'Night\'')['xTicks'].tolist()
    zDayTrans = dfxTicks.query('ZeitTransition == \'Day\'')['xTicks'].tolist()

    for i in zDayTrans:
        ax1.axvline(x=i, color='yellow', linestyle='--')

    for i in zNightTrans:
        ax1.axvline(x=i, color='blue', linestyle='--')

#
#
## Metrics

def interpulseIntervalFigure(jelly_title, axis, dfComplex, show_title = True, show_xLabels = True):
    df = dfComplex[dfComplex.InterpulseInterval.notnull() & (dfComplex['InterpulseInterval'] < 30)]
    ax = axis

    x = df['ZeitgeberTime']

    y = df['InterpulseInterval']

    ax.plot(x, y, c = 'k', lw = 2, label= 'average');

    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='Interpulse Time (s)')

    ax.grid(axis = 'y', alpha=0.5, linestyle='--')

    # ax.semilogy()

    ax.margins(x=0)

    ax.set_ylim(0, 3)

    if show_xLabels:
        ax.set_xticklabels(x, rotation='vertical')
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


def ysensativity (dataframe, metric):
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


def sensativityCCFigure(jelly_title, axis, dfComplex, show_title = True, show_xLabels = True, show_Legend = True):

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



    x = ysensativity(df, 'CenterChangedAfterS1')['min time'].tolist()

    x = [str(i) for i in x]

    x = [i[:i.find('.')] for i in x]


    yA1S1 = ysensativity(df, 'CenterChangedAfterS1')['count'].rolling(window=windowSize).mean()

    yA1S2 = ysensativity(df, 'CenterChangedAfterS2')['count'].rolling(window=windowSize).mean()

    yA1S3 = ysensativity(df, 'CenterChangedAfterS3')['count'].rolling(window=windowSize).mean()


    ax.plot(x, yA1S1, c = 'b', lw = 2, label= 'level of change 1 center after, s = 1');
    ax.plot(x, yA1S2, c = 'g', lw = 2, label= 'level of change 1 center after, s = 2');
    ax.plot(x, yA1S3, c = 'r', lw = 2, label= 'level of change 1 center after, s = 3');


    ax.axis(ymin = 0, ymax = 1)

    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% of pulses where center changed')

    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    if show_xLabels:
        ax.set_xticklabels(x, rotation='vertical')
    else:
        ax.get_xaxis().set_visible(False)

    if show_Legend: ax.legend()

    if show_title: ax.set_title(jelly_title + ' Jellyfish Centers Changed Sensativity Testing')


# In[39]:


def centersChangedFigure(jelly_title, axis, dfComplex, show_title = True, show_xLabels = True, show_Legend = True, sensativity = 3):

    ax = axis

    df = dfComplex[dfComplex.AbsoluteMinute.notnull()]

    #BINSIZE is number of minutes to use in each bin
    BINSIZE = 5


    #establishes column to groupby and use bins
    df['binCount'] = df['AbsoluteMinute']/BINSIZE
    df['counter'] = 1

    binCount = []
    for item in df['binCount']:
        binCount.append(int(item))

    df['binCount'] = binCount

    switcher = {
        1 : 'CenterChangedAfterS1',
        2 : 'CenterChangedAfterS2',
        3 : 'CenterChangedAfterS3',
    }


    dfFigure = ysensativity(df, switcher.get(sensativity))

    x = dfFigure['min time'].tolist()

    x = [str(i) for i in x]

    x = [i[:i.find('.')] for i in x]

    dfY = dfFigure['count']

    plotBinAverageWithErrorBars(dfY, x, ax, 20)

    ax.axis(ymin = 0, ymax = 1)

    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% of pulses where center changed')

    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    if show_xLabels:
        ax.set_xticklabels(x, rotation='vertical')
    else:
        ax.get_xaxis().set_visible(False)

    if show_Legend: ax.legend()

    if show_title: ax.set_title(jelly_title + ' Jellyfish Centers Changed Transition Metric (tests if center changed from one pulse to next)')

