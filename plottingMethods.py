
#current imports needed

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import math
import matplotlib.gridspec as gridspec
from scipy import stats

import figures as figures


# Helper Methods
def updateparameters():
    params = {'legend.fontsize': 'xx-large',
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
    pylab.rcParams.update(params)


# # Single Plots

# ### Metrics



def plotInterpulseInterval(outdir, jelly_title, dfComplex, dfxTicks, yfigurelen, xfigurelen):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing the interpulse-interval of a given jelly
    """

    updateparameters()
    # create empty figure
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    # generate interpulse figure with inputted data from complexDF
    figures.interpulseIntervalFigure(jelly_title, ax1, dfComplex, dfxTicks)

    #save fig
    outpath =  outdir / '{}_{}.png'.format(jelly_title, 'InterpulseInterval')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotInterpulseIntervalWithBar(outdir, jelly_title, dfComplex, dfxTicks, barArr, yfigurelen, xfigurelen):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing the interpulse-interval of a given jelly with day/night bar
    """
    updateparameters()
    # creates empty figure with inputted size
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [5, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    figures.bar4MovementDayNight(barArr, ax2)

    figures.interpulseIntervalFigure(jelly_title, ax1, dfComplex, dfxTicks)

    #save fig to outpath directory
    outpath =  outdir / '{}_{}.png'.format(jelly_title, 'plotInterpulseIntervalWithBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()



def plotCenterHistogramVertical(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing histogram of activity distribuiton by degree angle (bounded angle)
    """
    updateparameters()
    # generate empty figure
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax = fig.add_subplot(gs[0, 0])

    figures.initiatiorsHistogramFigure(jelly_title, ax, dfComplex)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterHistogramVertical')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()



def plotCenterHistogramHorizontal(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):
    updateparameters()
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing histogram of activity distribuiton by degree angle (bounded angle)
    """
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax = fig.add_subplot(gs[0, 0])


    figures.initiatiorsHistogramFigure(jelly_title, ax, dfComplex, vertical = False)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterHistogramHorizontal')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


# ### Centers

def plotActigram(outdir, jelly_title, dfActigram, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen, colormap):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing histogram of activity distribuiton by degree angle (bounded angle)
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, colormap)

    #save fig
    outpath = outdir / '{}_{}{}.png'.format(jelly_title, colormap.name, 'Actigram')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotSeismicActigram(outdir, jelly_title, dfActigram, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing seismic actigram
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.seismic)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'SeismicActigram')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()

def plotBinaryActigram(outdir, jelly_title, dfActigram, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
    """
    Input: complexDF
    Output: Binary (Black and White) Actigram determining degree of jellyfish pulse with a tick
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'BinaryActigram')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotActigramWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen, colormap):
    """
    # Is this being used?? (difference between this and binaryactigramwithbar?)
    Input: complexDF
    Output: Binary (Black and White) Actigram determining jellyfish pulse with a tick
    at its corresponding Zeitgeber time using the day/night plot bar
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [7, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    figures.bar4MovementDayNight(barArr, ax2)

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, colormap)

    #save fig
    outpath = outdir / '{}_{}{}.png'.format(jelly_title, colormap.name, 'ActigramWithBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotSeismicActigramWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
    """
    Input: complexDF
    Output: Actigram determining jellyfish pulse with a tick with additional intensity character for clustered pulses

    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [7, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    figures.bar4MovementDayNight(barArr, ax2)

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.seismic)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'SeismicActigramWithBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotBinaryActigramWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
# deboarh
    """
    Input: complexDF
    Output: Binary (Black and White) Actigram determining jellyfish pulse with a tick
    at its corresponding Zeitgeber time using the day/night plot bar
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [14, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    figures.bar4MovementDayNight(barArr, ax2)

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)


    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'BinaryActigramWithBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()

def plotBar(outdir, jelly_title, barArr, yfigurelen, xfigurelen):
    """
    Input: Complex Df
    Ouput: Day/Night Movement Bar, specifies when jellyfish have moved uses a red tick
    during the corresponding Zeitgeber time
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])

    figures.bar4MovementDayNight(barArr, ax1)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'plotBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


# ### Center Changed Metric


def plotSensativity(outdir, jelly_title, dfComplex, dfxTicks, yfigurelen, xfigurelen):

    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax = fig.add_subplot(gs[0, 0])

    figures.sensativityCCFigure(jelly_title, ax, dfComplex, dfxTicks)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Sensativity')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotCentersChanged(outdir, jelly_title, dfComplex, dfxTicks, yfigurelen, xfigurelen):
    """
    Input: complex dataframe for a given jellyfish
    Output: plots the % of pulses that have changed relative to a bounded angle and a given sensatitivy as defined by centersChangedFigure
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]
    gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

    # subplot
    ax = fig.add_subplot(gs[0, 0])

    figures.centersChangedFigure(jelly_title, ax, dfComplex, dfxTicks)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterChanged')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()

def plotSensativityWithBar(outdir, jelly_title, dfComplex, dfxTicks, barArr, yfigurelen, xfigurelen):
# xavier
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [4, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    figures.bar4MovementDayNight(barArr, ax2)

    figures.sensativityCCFigure(jelly_title, ax1, dfComplex, dfxTicks)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'SensativityWithBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotCentersChangedWithBar(outdir, jelly_title, dfComplex, dfxTicks, barArr, yfigurelen, xfigurelen):
    """
    Input: complex dataframe for a given jellyfish
    Output: plots the % of pulses that have changed relative to a bounded angle and a given sensatitivy as defined by centersChangedFigure
    Added Day Night Bar
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [4, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    figures.bar4MovementDayNight(barArr, ax2)

    figures.centersChangedFigure(jelly_title, ax1, dfComplex, dfxTicks)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterChangedWithBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()



# # Combined Plots


def ActigramANDInterpulseIntervalWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
"""
Input: ComplexDF
Ouput: Actigram figure with corresponding Interpulse Interval and Day/Night Bar
"""
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    #gridspec organization
    heights = [14, 1, 3]
    gs = fig.add_gridspec(ncols=1, nrows=3, height_ratios = heights)

    #subplot
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[1,0])
    ax3 = fig.add_subplot(gs[2,0])

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)
    figures.bar4MovementDayNight(barArr, ax2)
    figures.interpulseIntervalFigure(jelly_title, ax3, dfComplex, dfxTicks, show_title=False, show_xLabels=False)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'ActigramANDInterpulseInterval')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def Actigram_II_CC_AND_CHVertWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
# xavier
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    #gridspec organization
    heights = [15, 1, 3, 3]
    widths = [10, 1]
    gs = fig.add_gridspec(ncols=2, nrows=4, height_ratios = heights, width_ratios = widths)

    #subplot
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])
    fig_ax3 = fig.add_subplot(gs[2,0])
    fig_ax4 = fig.add_subplot(gs[3, 0])
    fig_ax5 = fig.add_subplot(gs[0,1])

    figures.actigramFigure(dfActigram, dfxTicks, fig_ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)
    figures.bar4MovementDayNight(barArr,  fig_ax2)
    figures.interpulseIntervalFigure(jelly_title, fig_ax3, dfComplex, dfxTicks, show_title=False, show_xLabels=False)
    figures.centersChangedFigure(jelly_title, fig_ax4, dfComplex, dfxTicks, show_title=False, show_xLabels=False, show_Legend=False)
    figures.initiatiorsHistogramFigure(jelly_title, fig_ax5, dfComplex, vertical=True, show_title=False, show_degreeLabels=False)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram_II_CC_AND_CHVert')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def Actigram_II_CC_AND_CHDayNightWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
# xavier
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    #gridspec organization
    heights = [15, 1, 5, 5]
    widths = [10, 1, 1]
    gs = fig.add_gridspec(ncols=3, nrows=4, height_ratios = heights, width_ratios = widths)

    #subplot
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])
    fig_ax3 = fig.add_subplot(gs[2,0])
    fig_ax4 = fig.add_subplot(gs[3, 0])
    fig_ax5 = fig.add_subplot(gs[0,1])
    fig_ax6 = fig.add_subplot(gs[0,2])

    figures.actigramFigure(dfActigram, dfxTicks, fig_ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)
    figures.bar4MovementDayNight(barArr,  fig_ax2)
    figures.interpulseIntervalFigure(jelly_title, fig_ax3, dfComplex, dfxTicks, show_title=False, show_xLabels=False)
    figures.centersChangedFigure(jelly_title, fig_ax4, dfComplex, dfxTicks, show_title=False, show_xLabels=False, show_Legend=False)

    figures.initiatiorsHistogramQueryFigure('Day', fig_ax5, dfComplex, 'DayOrNight == \'Day\'', show_title=True, show_degreeLabels=False)
    figures.initiatiorsHistogramQueryFigure('Night', fig_ax6, dfComplex, 'DayOrNight == \'Night\'', show_title=True, show_degreeLabels=False)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram_II_CC_AND_CHDayNight')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def centersHistogramDayANDNightPlot(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing distribution of centers by degree angle for one day and night period
    """
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    #gridspec organization
    heights = [1, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios = heights)

    #subplot
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])

    figures.initiatiorsHistogramQueryFigure('Day', fig_ax1, dfComplex, 'DayOrNight == \'Day\'', vertical=False, show_title=True,
                                            show_degreeLabels=True)
    figures.initiatiorsHistogramQueryFigure('Night', fig_ax2, dfComplex, 'DayOrNight == \'Night\'', vertical=False, show_title=True,
                                            show_degreeLabels=True)

    fig.suptitle(jelly_title)

    #save fig
    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'centersHistogramDayANDNightPlot')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


##############################################################

##############################################################

##############################################################

def main(jelly_title, outdir, dfActigram, barArr, dfxTicks, dfComplex, RHOPOS, RHOLAB, stdYlen = None, stdXlen = None):
    """

    :param jelly_title: name of jellyfish
    :param outdir: output directory where png's will be saved
    :param dfActigram:actigram created by figures.py
    :param barArr:bar array created by DataFrameCreationMethods.py
    :param dfxTicks: x ticks for image axis
    :param dfComplex:complex DF
    :param RHOPOS:rhopalia position
    :param RHOLAB:rhopalia label
    :return:
    """



    #standard graph sizes
    if stdYlen is None: stdYlen = 15/3
    if stdXlen is None: stdXlen = dfComplex['AbsoluteMinute'].max()/60*5/3

    # without bar

    plotInterpulseInterval(outdir, jelly_title, dfComplex, dfxTicks, 7, stdXlen)

    plotCenterHistogramVertical(outdir, jelly_title, dfComplex, 36, 10)

    plotCenterHistogramHorizontal(outdir, jelly_title, dfComplex, 10, 36)

    plotSeismicActigram(outdir, jelly_title, dfActigram, dfxTicks, RHOPOS, RHOLAB, stdYlen, stdXlen)

    plotBinaryActigram(outdir, jelly_title, dfActigram, dfxTicks, RHOPOS, RHOLAB, 7, stdXlen)

    # plotSensativity(outdir, jelly_title, dfComplex, dfxTicks, 7, stdXlen)

    plotCentersChanged(outdir, jelly_title, dfComplex, dfxTicks, 7, stdXlen)

    # with bar

    plotInterpulseIntervalWithBar(outdir, jelly_title, dfComplex, dfxTicks, barArr, 7, stdXlen)

    plotSeismicActigramWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, RHOPOS, RHOLAB, stdYlen, stdXlen)

    plotBinaryActigramWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, RHOPOS, RHOLAB, 7, stdXlen)

    # plotSensativityWithBar(outdir, jelly_title, dfComplex, dfxTicks, barArr, 7, stdXlen)

    plotCentersChangedWithBar(outdir, jelly_title, dfComplex, dfxTicks, barArr, 7, stdXlen)

    # combined

    ActigramANDInterpulseIntervalWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, dfComplex, RHOPOS, RHOLAB, 7, stdXlen)

    Actigram_II_CC_AND_CHVertWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, dfComplex, RHOPOS, RHOLAB, 17, stdXlen)

    Actigram_II_CC_AND_CHDayNightWithBar(outdir, jelly_title, dfActigram, barArr, dfxTicks, dfComplex, RHOPOS, RHOLAB, 17, stdXlen)

    centersHistogramDayANDNightPlot(outdir, jelly_title, dfComplex, 20, 36)

    plotBar(outdir, jelly_title, barArr, 2, stdXlen)
