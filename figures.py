

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


###  Definitions, look at () for ex so i remember what is what for now -deb ###
# bar4MovementDayNight- the skinny bar with the yellow/blue day/night, and the red ticks for movement // (plotBar)
# actigramFigure- the blue graph with time vs degrees // (SeismicActigram)
# interpulseIntervalFigure- the spikey grey one with the blue line going through the middle // (InterpulseInterval)
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


def bar4MovementDayNight(dfBar, ax, width = 4):
    """
    Creates DayNight movement bar to go along with actigram and other behavioral figures.

    :param dfBar: Bar dataframe, created in DataFrameCreationMethods. Image array specifying what is
    :param ax: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param width: width of the bar. specified in the creation of the bar.
    :return: axes object filled with bar image.
    """
    # takes slice of bar to compress the image to be manageable for our purposes
    # takes every 10th row of the bar to create a sliced image
    dfBar = cdf.createCompressedMovementDayNightBar(dfBar, 10)

    # imshow == Image show. Shows the np array as an image.
    # np.transpose flips the array from vertical to horizontal. It goes from being n frames long to n frames wide
    ax.imshow(np.transpose(dfBar, (1, 0, 2)), origin='lower', aspect='auto')

    # labels the Day/Night section on the top half and the Movement section on the bottom half of the plotBar
    ax.set_yticks([width/4, width*3/4])
    ax.set_yticklabels(['Movement', 'Light or Dark'])

    # x axis not visible 
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

    # renames axes object for convenience
    ax1 = axis

    # imshow function - show the sliced actogram; .T flips rows and columns, bcuz it's a transposed array(?). x
    ax1.imshow(dfActigramComp.T, origin='lower', aspect='auto', cmap=colormap, interpolation='bilinear')

    # if statement setting y ticks, both axis  x
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

        # axis labels, both y's and x
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

    # grids. Changes colors so that grids show regardless of colormap.
    # colormaps
    # binary: black and white
    # seismic: dark blues
    if colormap == cm.binary:
        ax1.grid(which='major', color='#bebeff', linestyle=':', linewidth=1)
    elif colormap == cm.seismic:
        ax1.grid(which='major', color='w', linestyle=':', linewidth=1)
    else:
        ax1.grid(which='major', color='#7f7f7f', linestyle=':', linewidth=1)

    #setting x ticks
    justXticks = dfxTicksComp[dfxTicksComp.TickType == 'hour_relative']  # I get what is says but not what it does 4: rest of function   x

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

    # takes pulses where Interpulse interval is not null [and is lower than thirty?  x]
    df = dfComplex[dfComplex.InterpulseInterval.notnull() & (dfComplex.InterpulseInterval < 30)]

    # renames axes object for convenience
    ax = axis

    # global frame taken from complex dataframe (line sets x to the dataframe column with that label  x)
    # global frame taken from complex dataframe for x axis data
    x = df['global frame']

    # interpulse interval taken from dataframe for y axis data
    y = df['InterpulseInterval']

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
        justXticks = dfxTicks[dfxTicks.TickType == 'hour_absolute']
    # fills each xtick version with the contents of the named column   x
        xTicks = justXticks['xTicks'].tolist()
        xTickLabels = justXticks['xTickLabels'].tolist()

        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels)

    else:
        ax.get_xaxis().set_visible(False)  # don't bother doing that^ if we're not gonna see it

    if show_title: ax.set_title(jelly_title + '- Interpulse Interval')

def initiatiorsHistogramFigure(jelly_title, ax, dfComplex, vertical = True, show_title = True, show_degreeLabels = True):
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
    :return: axes object filled with IPI figure.
    """

    # aggregates angle measurements from 'bounded angle' column
    dfGrouped = dfComplex.groupby(['bounded angle'])['bounded angle'].agg('count')

    degrees = dfGrouped.index.tolist()  # sets 'degrees' as contents of dfGrouped, in list form   x
    counts = dfGrouped.tolist()  # populates 'counts' with dfGrouped in index form.  possibe it's vice versa but I dont think so  x
    numPulses = sum(counts)

    # normalizes the amount into percent of pulses  [Konnor is a great speller, what are you talking about]
    percents = [i/numPulses for i in counts]

    # interesting, this originally makes a horizontal/vertical bar plot;
    # what's the math diff between this and using Hist()?   x [something to do with the normalization?]
    # For CenterHistogramVertical
    # The graph itself is vertical, but the bars are horizontal
    if vertical:
        # create horizontal bar plot
        ax.barh(degrees, percents)

         # x axis label: % of total counts
        ax.set_xlabel(xlabel=r'% of total counts')

        ax.margins(y=0)

         # y axis label: Degree
        if show_degreeLabels:
            ax.set_ylabel(ylabel='Degree')
        else:
            ax.get_yaxis().set_visible(False)
    
    # For CenterHistogramHorizontal
    # The graph itself is horizontal, but the bars are vertical
    else:
        # create vertical bar plot
        ax.bar(degrees, percents)

         # y axis label: % of total counts
        ax.set_ylabel(ylabel=r'% of total counts')

        ax.margins(x=0)

         # x axis label: Degree
        if show_degreeLabels:
            ax.set_xlabel(xlabel='Degree')
        else:
            ax.get_xaxis().set_visible(False)

    if show_title: ax.set_title(jelly_title)


def initiatiorsHistogramQueryFigure(jelly_title, ax, dfComplex, question, vertical=True, show_title=True, show_degreeLabels = True):
    """
    lets you query the complex dataframe data to look at differences in subsets of data. Filtered Complex DF is an input
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

    # queries the complex DF depending on the "question" input to filter based on what we want to see in the graph
    dfQuery = dfComplex.query(question)

    initiatiorsHistogramFigure(jelly_title, ax, dfQuery, vertical, show_title, show_degreeLabels)


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

    # plot metric? bar in a thicker black 
    # plot error bars above and below the average in a thinner blue line
    ax.plot(x, ym, c = 'k', lw = 2, label= 'Metric');
    ax.plot(x, ya, c = 'b', lw = 0.5, label='Standard Error Above Average');
    ax.plot(x, yb, c = 'b', lw = 0.5, label='Standard Error Below Average');

    ax.fill_between(x = x, y1 = ya, y2 = yb, color = fillColor, alpha = fillShade)


def sensitivityCCFigure(jelly_title, axis, dfComplex, dfxTicks, show_title = True, show_xLabels = True, show_Legend = True):
    """
    Plots the different sensitivities of the center changed figure. S10, S20, S30 are all plotted together. [konnorspellsgrate]
    Does not seem to be working rn?
    TODO: fix sensitivityCCFigure.

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and all of the CenterChangedS** columns.
    :param dfxTicks: Xtick dataframe, initialized in DataFrameCreationMethods
    :param show_title: True if title is desired, False otherwise. Default is True. same for two below   x
    :param show_xLabels:
    :param show_Legend:
    :return:
    """

    # renames axes object for convenience
    ax = axis
    # pull AbsoluteMinute data from Complex DF
    df = dfComplex[dfComplex.AbsoluteMinute.notnull()]

    #BINSIZE is number of minutes to use in each bin
    BINSIZE = 5
    colorDN = 'b'
    colorND = '#fcd12a'
    windowSize = 20

    #establishes column to group by and use bins
    df['binCount'] = df['AbsoluteMinute']/BINSIZE
    df['counter'] = 1

    binCount = []
    for item in df['binCount']:  # gives a number to each resident of binCount?  x
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

    ax.plot(x, yA1S1, c = 'b', lw = 2, label= 'level of change 1 center after, s = 1');  # should i nix the ;?  x
    ax.plot(x, yA1S2, c = 'g', lw = 2, label= 'level of change 1 center after, s = 2');
    ax.plot(x, yA1S3, c = 'r', lw = 2, label= 'level of change 1 center after, s = 3');


    ax.axis(ymin = 0, ymax = 1)

    # axis labels, both y's and x
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% pulses IC')

    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels - nearly identical to this section in centersChangedFigure   x
    if show_xLabels:
        lastx = x[-1]

        compressionFactor = dfxTicks[dfxTicks.TickType == 'hour_absolute'].iloc[0, 0] / lastx

        justXticks = dfxTicks[dfxTicks.TickType == 'hour_absolute']

        justXticks['xTicks'] = justXticks['xTicks'] / compressionFactor

        xTicks = justXticks['xTicks'].tolist()
        xTickLabels = justXticks['xTickLabels'].tolist()

        # axis labels, both y's and x
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
    Very similar to the sensativities figure although it only ______

    "centers" describes the angle of a pulse, specifically the bounded angle. If the bounded angle of the next pulse is
    within the sensitivity distance, ______
    
    TODO: refactor the columns involved to say "AngleChangedS10"
    TODO: change this so it is the inverse, and a measure of centralization, not decentralization
    TODO: We're not in Kansas anymore!

    :param jelly_title: title of Jellyfish to be used in naming of figure
    :param axis: axes object (from matplotlib Axes class) that has been initialized by subplot or gridspec.
    :param dfComplex: Takes in the complex dataframe. Uses the global frame and all of the CenterChangedS** columns.
    :param dfxTicks: Xtick dataframe, initialized in DataFrameCreationMethods
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

    # renames axes object for convenience
    ax = axis

    # filters the dataframe [to fill 'df' with every cell from AbsoluteMinute with any value present? i think?   x]
    df = dfComplex[dfComplex.AbsoluteMinute.notnull()]

    # BINSIZE is number of minutes to use in each bin
    # WINDOWSIZE is the number of bins to use in the rolling average and standard error analysis
    # create 3 different sizes of figures: Long, Medium, and Short
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
    plotBinAverageWithErrorBars(dfY, x, ax, WINDOWSIZE)  # unsure- is this initializing an array or something, or missing a . after plot?   x

    # sets y bounds using input
    ax.axis(ymin = bounds[0], ymax = bounds[1])

    # sets labels, x and y
    ax.set_xlabel(xlabel=r'Zeitgeber Time')
    ax.set_ylabel(ylabel='% pulses IC')

    # sets grid
    ax.grid(axis = 'y', alpha=0.5, linestyle='--')
    ax.margins(x=0)

    # x ticks and labels
    if show_xLabels:
        lastx = x[-1]  # havent found anything about the [-1] thing; extracting the last item in the list?  x

        lastFrame = dfComplex.iloc[-1]['global frame']
        #lastFrame = dfxTicks[dfxTicks.TickType == 'LastFrame'].iloc[0, 0]

        compressionFactor = lastFrame / lastx

        justXticks = dfxTicks[dfxTicks.TickType == 'hour_absolute']

        justXticks['xTicks'] = justXticks['xTicks'] / compressionFactor

        xTicks = justXticks['xTicks'].tolist()
        xTickLabels = justXticks['xTickLabels'].tolist()

        # set x ticks and x label
        ax.set_xticks(xTicks)
        ax.set_xticklabels(xTickLabels)

    else:
        ax.get_xaxis().set_visible(False)

    if show_Legend: ax.legend()

    # create title
    if show_title: ax.set_title(jelly_title + ' Interpulse Change')

