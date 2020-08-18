
#current imports needed

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import math
import matplotlib.gridspec as gridspec
from scipy import stats

import figures2 as figures


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


def plotInterpulseInterval(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):

    updateparameters()

    #subplot
    fig, ax = plt.subplots(1, figsize=(xfigurelen, yfigurelen))

    figures.interpulseIntervalFigure(jelly_title, ax, dfComplex)

    #save fig
    outpath =  outdir / '{}_{}.png'.format(jelly_title, 'InterpulseInterval')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()



def plotCenterHistogramVertical(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):
    updateparameters()

    #subplot
    fig, ax = plt.subplots(1, figsize=(xfigurelen, yfigurelen))

    figures.initiatiorsHistogramFigure(jelly_title, ax, dfComplex)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterHistogramVertical')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()



def plotCenterHistogramHorizontal(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):
    updateparameters()

    #subplot
    fig, ax = plt.subplots(1, figsize=(xfigurelen, yfigurelen))


    figures.initiatiorsHistogramFigure(jelly_title, ax, dfComplex, vertical = False)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterHistogramHorizontal')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


# ### Centers

def plotActigram(outdir, jelly_title, dfActigram, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen, colormap):

    updateparameters()

    #subplot
    fig, ax1 = plt.subplots(1,figsize=(xfigurelen, yfigurelen))

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, colormap)

    #save fig
    outpath = outdir / '{}_{}{}.png'.format(jelly_title, colormap.name, 'Actigram')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotSeismicActigram(outdir, jelly_title, dfActigram, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):

    updateparameters()

    #subplot
    fig, ax1 = plt.subplots(1,figsize=(xfigurelen, yfigurelen))

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.seismic)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'SeismicActigram')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()

def plotBinaryActigram(outdir, jelly_title, dfActigram, dfxTicks, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):

    updateparameters()

    #subplot
    fig, ax1 = plt.subplots(1,figsize=(xfigurelen, yfigurelen))

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'BinaryActigram')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


# ### Center Changed Metric


def plotSensativity(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):

    updateparameters()

    #subplot
    fig, ax = plt.subplots(1, figsize=(xfigurelen, yfigurelen))

    figures.sensativityCCFigure(jelly_title, ax, dfComplex)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Sensativity')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotCentersChanged(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):

    updateparameters()

    #subplot
    fig, ax = plt.subplots(1, figsize=(xfigurelen, yfigurelen))

    figures.centersChangedFigure(jelly_title, ax, dfComplex)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterChanged')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()



# # Combined Plots


def ActigramANDInterpulseInterval(outdir, jelly_title, dfActigram, dfxTicks, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):

    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen))

    #gridspec organization
    heights = [3, 1]
    gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios = heights)

    #subplot
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[1,0])

    figures.actigramFigure(dfActigram, dfxTicks, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)
    figures.interpulseIntervalFigure(jelly_title, ax2, dfComplex, show_title=False, show_xLabels=False)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'ActigramANDInterpulseInterval')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def Actigram_II_CC_AND_CHVert(outdir, jelly_title, dfActigram, dfxTicks, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):

    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen))

    #gridspec organization
    heights = [3, 1, 1]
    widths = [10, 1]
    gs = fig.add_gridspec(ncols=2, nrows=3, height_ratios = heights, width_ratios = widths)

    #subplot
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])
    fig_ax3 = fig.add_subplot(gs[2,0])
    fig_ax4 = fig.add_subplot(gs[0,1])

    figures.actigramFigure(dfActigram, dfxTicks, fig_ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)
    figures.interpulseIntervalFigure(jelly_title, fig_ax2, dfComplex, show_title=False, show_xLabels=False)
    figures.centersChangedFigure(jelly_title, fig_ax3, dfComplex, show_title=False, show_xLabels=False, show_Legend=True)
    figures.initiatiorsHistogramFigure(jelly_title, fig_ax4, dfComplex, vertical=True, show_title=False, show_degreeLabels=False)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram_II_CC_AND_CHVert')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def Actigram_II_CC_AND_CHDayNight(outdir, jelly_title, dfActigram, dfxTicks, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):

    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen))

    #gridspec organization
    heights = [3, 1, 1]
    widths = [10, 1, 1]
    gs = fig.add_gridspec(ncols=3, nrows=3, height_ratios = heights, width_ratios = widths)

    #subplot
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])
    fig_ax3 = fig.add_subplot(gs[2,0])
    fig_ax4 = fig.add_subplot(gs[0,1])
    fig_ax5 = fig.add_subplot(gs[0,2])

    figures.actigramFigure(dfActigram, dfxTicks, fig_ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels, cm.binary)
    figures.interpulseIntervalFigure(jelly_title, fig_ax2, dfComplex, show_title=False, show_xLabels=False)
    figures.centersChangedFigure(jelly_title, fig_ax3, dfComplex, show_title=False, show_xLabels=False, show_Legend=True)

    figures.initiatiorsHistogramQueryFigure('Day', fig_ax4, dfComplex, 'DayOrNight == \'Day\'', show_title=True, show_degreeLabels=False)
    figures.initiatiorsHistogramQueryFigure('Night', fig_ax5, dfComplex, 'DayOrNight == \'Night\'', show_title=True, show_degreeLabels=False)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram_II_CC_AND_CHDayNight')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def centersHistogramDayANDNightPlot(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):

    fig = plt.figure(figsize=(xfigurelen, yfigurelen))

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

def main(jelly_title, outdir, dfActigram, dfxTicks, dfComplex, RHOPOS, RHOLAB):

    #standard graph sizes
    stdYlen = 15/3
    stdXlen = dfComplex['AbsoluteMinute'].max()/60*5/3

    plotInterpulseInterval(outdir, jelly_title, dfComplex, 3, stdXlen)

    plotCenterHistogramVertical(outdir, jelly_title, dfComplex, 36, 10)

    plotCenterHistogramHorizontal(outdir, jelly_title, dfComplex, 10, 36)

    plotSeismicActigram(outdir, jelly_title, dfActigram, dfxTicks, RHOPOS, RHOLAB, stdYlen, stdXlen)

    plotBinaryActigram(outdir, jelly_title, dfActigram, dfxTicks, RHOPOS, RHOLAB, 7, stdXlen)

    plotSensativity(outdir, jelly_title, dfComplex, 3, stdXlen)

    plotCentersChanged(outdir, jelly_title, dfComplex, 3, stdXlen)

    ActigramANDInterpulseInterval(outdir, jelly_title, dfActigram, dfxTicks, dfComplex, RHOPOS, RHOLAB, 7, stdXlen)

    Actigram_II_CC_AND_CHVert(outdir, jelly_title, dfActigram, dfxTicks, dfComplex, RHOPOS, RHOLAB, 10, stdXlen)

    Actigram_II_CC_AND_CHDayNight(outdir, jelly_title, dfActigram, dfxTicks, dfComplex, RHOPOS, RHOLAB, 10, stdXlen)

    centersHistogramDayANDNightPlot(outdir, jelly_title, dfComplex, 20, 36)




