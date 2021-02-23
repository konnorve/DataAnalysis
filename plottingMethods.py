
#current imports needed

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
# import seaborn as sns; sns.set() # pretty plotting... hopefully?... maybe not...
import matplotlib.cm as cm
import imageio
import os

from . import DataFrameCreationMethods as cdf
from . import figures


# Helper Methods
def updateparameters():
    params = {'legend.fontsize': 'xx-large',
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
    pylab.rcParams.update(params)


# # Single Plots

def plotInterpulseInterval(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen, plotBar=True):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing the interpulse-interval of a given jelly
    """

    updateparameters()
    # create empty figure
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)
    # "constrained_layout" automatically adjusts subplots to fit window size

    if plotBar:
        # gridspec organization
        heights = [5, 1]
        gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

        # subplot
        ax2 = fig.add_subplot(gs[1, 0])

        figures.bar4MovementDayNight(dfComplex, ax2)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'InterpulseIntervalWithBar')

    else:
        # gridspec organization
        heights = [1]
        gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'InterpulseInterval')

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    # generate interpulse figure with inputted data from complexDF
    figures.interpulseInterval(jelly_title, ax1, dfComplex)

    #save fig
    fig.savefig(str(outpath),bbox_inches='tight')
    # "bbox_inches" removes extra whitespace from around the rendered figure.
    plt.close()


def plotPulseRate(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen, plotBar=True):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing the Pulse Rate of a given jelly
    """

    updateparameters()
    # create empty figure
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)
    # "constrained_layout" automatically adjusts subplots to fit window size

    if plotBar:
        # gridspec organization
        heights = [5, 1]
        gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

        # subplot
        ax2 = fig.add_subplot(gs[1, 0])

        figures.bar4MovementDayNight(dfComplex, ax2)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'PulseRateWithBar')

    else:
        # gridspec organization
        heights = [1]
        gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'PulseRate')

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    # generate pulse rate figure with inputted data from complexDF
    figures.pulseRate(jelly_title, ax1, dfComplex)

    #save fig
    fig.savefig(str(outpath),bbox_inches='tight')
    # "bbox_inches" removes extra whitespace from around the rendered figure.
    plt.close()


def plotDistanceMoved(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen, plotBar=True):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing the Distance Moved of a given jelly
    """

    updateparameters()
    # create empty figure
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)
    # "constrained_layout" automatically adjusts subplots to fit window size

    if plotBar:
        # gridspec organization
        heights = [5, 1]
        gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

        # subplot
        ax2 = fig.add_subplot(gs[1, 0])

        figures.bar4MovementDayNight(dfComplex, ax2)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'DistanceMovedWithBar')

    else:
        # gridspec organization
        heights = [1]
        gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'DistanceMoved')

    # subplot
    ax1 = fig.add_subplot(gs[0, 0])
    # generate pulse rate figure with inputted data from complexDF
    figures.distanceMoved(jelly_title, ax1, dfComplex)

    #save fig
    fig.savefig(str(outpath),bbox_inches='tight')
    # "bbox_inches" removes extra whitespace from around the rendered figure.
    plt.close()


def plotAngleHistogramVertical(outdir, jelly_title, dfComplex, rhopos, rholab, yfigurelen, xfigurelen, hist_constraints=[]):
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

    figures.initiatiorsHistogramFigure(jelly_title, ax, dfComplex,rhopos,rholab, constraints=hist_constraints)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterHistogramVertical')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()



def plotAngleHistogramHorizontal(outdir, jelly_title, dfComplex, rhopos, rholab, yfigurelen, xfigurelen, hist_constraints=[]):
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

    # adding the initiatorHist fig to the current plot?
    figures.initiatiorsHistogramFigure(jelly_title, ax, dfComplex, rhopos, rholab, vertical = False, constraints=hist_constraints)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterHistogramHorizontal')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


# ### Centers

def plotHistorgram4DayHourSlices(outdir, jelly_title, dfComplex, rhopos, rholab, yfigurelen, xfigurelen, hist_constraints=[]):
    updateparameters()
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing histogram of activity distribuiton by degree angle (bounded angle)
    """

    dfComplex["Day.Hour"] = dfComplex["ZeitgeberDay"].astype(str) + str('.') + dfComplex["ZeitgeberHour"].astype(str)

    uniqueCombos = dfComplex["Day.Hour"].unique()

    fig = plt.figure(figsize=(xfigurelen, len(uniqueCombos)*yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]*len(uniqueCombos)
    widths = [xfigurelen, 2]
    gs = fig.add_gridspec(ncols=2, nrows=len(uniqueCombos), height_ratios=heights, width_ratios=widths)

    # subplot
    for i, combo in enumerate(uniqueCombos):
        print(combo)

        ax1 = fig.add_subplot(gs[i, 0])
        ax2 = fig.add_subplot(gs[i, 1])

        dfSlice = dfComplex.loc[dfComplex['Day.Hour'] == combo]

        day = dfSlice["ZeitgeberDay"].iloc[0]
        hour = dfSlice["ZeitgeberHour"].iloc[0]

        ax2.text(0, 0.5, '{} {:02}:00'.format(day, hour), size='xx-large')
        ax2.axis("off")

        # adding the initiatorHist fig to the current plot?
        if i == 0:
            sjdl = False
            sjrl = True
        elif i == len(uniqueCombos) - 1:
            sjdl = True
            sjrl = False
        else:
            sjdl = False
            sjrl = False

        figures.initiatiorsHistogramFigure(combo, ax1, dfSlice, rhopos, rholab, vertical=False, show_title=False,
                                           show_degreeLabels=False,
                                           show_just_degree_labels=sjdl,
                                           show_just_rhopalia_labels=sjrl,
                                           constraints=hist_constraints)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Histogram4DayHourSlices')
    fig.savefig(str(outpath), bbox_inches='tight')

    plt.close()


def plotHistorgram4DayLightSlices(outdir, jelly_title, dfComplex, rhopos, rholab, yfigurelen, xfigurelen, hist_constraints=[]):
    updateparameters()
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing histogram of activity distribuiton by degree angle (bounded angle)
    """

    dfComplex["Day.LightCycle"] = dfComplex["ZeitgeberDay"].astype(str) + str('.') + dfComplex["DayOrNight"].astype(str)

    uniqueCombos = dfComplex["Day.LightCycle"].unique()

    fig = plt.figure(figsize=(xfigurelen, len(uniqueCombos)*yfigurelen), constrained_layout=True)

    # gridspec organization
    heights = [1]*len(uniqueCombos)
    widths = [xfigurelen, 2]
    gs = fig.add_gridspec(ncols=2, nrows=len(uniqueCombos), height_ratios=heights, width_ratios=widths)

    # subplot
    for i, combo in enumerate(uniqueCombos):
        print(combo)

        ax1 = fig.add_subplot(gs[i, 0])
        ax2 = fig.add_subplot(gs[i, 1])

        dfSlice = dfComplex.loc[dfComplex['Day.LightCycle'] == combo]

        day = dfSlice["ZeitgeberDay"].iloc[0]
        lightcycle = dfSlice["DayOrNight"].iloc[0]

        ax2.text(0, 0.5, '{} {}'.format(day, lightcycle), size='xx-large')
        ax2.axis("off")

        # adding the initiatorHist fig to the current plot?
        if i == 0:
            sjdl = False
            sjrl = True
        elif i == len(uniqueCombos) - 1:
            sjdl = True
            sjrl = False
        else:
            sjdl = False
            sjrl = False

        figures.initiatiorsHistogramFigure(combo, ax1, dfSlice, rhopos, rholab, vertical=False, show_title=False,
                                           show_degreeLabels=False,
                                           show_just_degree_labels=sjdl,
                                           show_just_rhopalia_labels=sjrl,
                                           constraints=hist_constraints)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Histogram4DayLightSlices')
    fig.savefig(str(outpath), bbox_inches='tight')

    plt.close()


def plotJellyTrajectory(outdir, jelly_title, dfComplex, distanceMovedThreshold=50, image_max_x=640, image_max_y=480):
    complexDFfiltered = dfComplex.loc[dfComplex['DistanceMoved_After'] < distanceMovedThreshold]

    fig, ax = plt.subplots(figsize=(image_max_x / 50, image_max_y / 50))

    ax.set_title(jelly_title)

    figures.jelly_trajectory(complexDFfiltered, fig, ax, image_max_x, image_max_y, a=0.4)

    plt.savefig(outdir / '{}_jelly_trajectory.png'.format(jelly_title))


def plotJellyTrajectoryDayNight(outdir, jelly_title, dfComplex, distanceMovedThreshold=50, image_max_x=640,
                                image_max_y=480):
    complexDFfiltered = dfComplex.loc[dfComplex['DistanceMoved_After'] < distanceMovedThreshold]

    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex='all', figsize=(image_max_x / 50, image_max_y / 25))
    ax1.set_title("{} Day".format(jelly_title))
    ax2.set_title("{} Night".format(jelly_title))

    complexDFDaySegments = complexDFfiltered.loc[complexDFfiltered['DayOrNight'] == 'Day']
    complexDFNightSegments = complexDFfiltered.loc[complexDFfiltered['DayOrNight'] == 'Night']

    figures.jelly_trajectory(complexDFDaySegments, fig, ax1, image_max_x, image_max_y, a=0.4)
    figures.jelly_trajectory(complexDFNightSegments, fig, ax2, image_max_x, image_max_y, a=0.4)

    plt.savefig(outdir / '{}_jelly_trajectory_daynight.png'.format(jelly_title))


def plotJellyTrajectoryFiltered(outdir, jelly_title, dfComplex, column_name, distanceMovedThreshold=50, image_max_x=640,
                                image_max_y=480):
    complexDFfiltered = dfComplex.loc[dfComplex['DistanceMoved_After'] < distanceMovedThreshold]

    unique_vars = complexDFfiltered[column_name].unique()

    fig, axes = plt.subplots(nrows=len(unique_vars), sharex='all',
                             figsize=(image_max_x / 50, image_max_y * len(unique_vars) / 50))

    for ax, var in zip(axes, unique_vars):
        ax.set_title("{} {}".format(jelly_title, var))

        complexDFslice = complexDFfiltered.loc[complexDFfiltered[column_name] == var]

        figures.jelly_trajectory(complexDFslice, fig, ax, image_max_x, image_max_y, a=0.4)

    plt.savefig(outdir / '{}_jelly_trajectory_{}.png'.format(jelly_title, column_name))


def create_trajectory_gif(complexDFslice, jelly_title, outDir, distanceMovedThreshold=50, a=0.4, image_max_x=640,
                          image_max_y=480):
    complexDFfiltered = complexDFslice.loc[complexDFslice['DistanceMoved_After'] < distanceMovedThreshold]

    x_arr = complexDFfiltered['centroid x'].to_numpy()
    y_arr = complexDFfiltered['centroid y'].to_numpy()
    # converts Zeitgeber time into int (epoch time)
    time_arr = complexDFfiltered['ZeitgeberTime'].astype(int).to_numpy()

    # shape all the coordinate points into segments to plot continuous line
    points = np.array([x_arr, y_arr]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    gif_frames = np.linspace(0, len(time_arr), 100, dtype=int)
    gif_frame_paths = [outDir / '{}.png'.format(i) for i in gif_frames]

    fig, ax = plt.subplots(figsize=(image_max_x / 50, image_max_y / 50))
    ax.set_title(jelly_title)
    ax.set_xlim(0, image_max_x)
    ax.set_ylim(0, image_max_y)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(time_arr.min(), time_arr.max())

    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.viridis), ax=ax)

    for n in range(1, len(gif_frames)):
        print(n)

        start = gif_frames[n - 1]
        end = gif_frames[n]
        path = gif_frame_paths[n]

        lc = LineCollection(segments[start:end], cmap='viridis', norm=norm, alpha=a)  # change opacity with alpha

        # Set the values used for colormapping
        lc.set_array(time_arr[start:end])
        lc.set_linewidth(2)
        line = ax.add_collection(lc)

        # normalize the color scale to the color map
        cmap = cm.viridis

        # color a portion of the color scale according to the normalized colors we've set
        for i in range(len(time_arr[start:end])):
            color = cmap(norm(time_arr[start + i]))
            ax.plot(x_arr[start + i], y_arr[start + i], marker='o', c=color, alpha=a)

        # labelling stuff
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')

        plt.savefig(path)

    plt.savefig(outDir / '{}_trajectory_plot_final.png'.format(jelly_title))

    gif_frame_paths.pop(0)

    # build gif
    with imageio.get_writer(outDir / '{}_trajectory_movie.gif'.format(jelly_title), mode='I') as writer:
        for filename in gif_frame_paths:
            image = imageio.imread(filename)
            writer.append_data(image)
        final_image = imageio.imread(gif_frame_paths[-1])
        for i in range(20):
            writer.append_data(final_image)

            # Remove files
    for filename in set(gif_frame_paths):
        os.remove(filename)


def plotActigram(outdir, jelly_title, dfActigram, complexDF, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen, plotBar=True):
    """
    Input: complex dataframe for a jellyfish
    Output: figure vizualizing histogram of activity distribuiton by degree angle (bounded angle)
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)
    if plotBar:
        # gridspec organization
        heights = [7, 1]
        gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

        # plotting bar
        ax2 = fig.add_subplot(gs[1, 0])
        figures.bar4MovementDayNight(complexDF, ax2)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'ActigramWithBar')
    else:
        # gridspec organization
        heights = [1]
        gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

        outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram')

    # actigram plotting on gridspec
    ax1 = fig.add_subplot(gs[0, 0])
    figures.actigramFigure(dfActigram, complexDF, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels)

    #save fig
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotCentralization(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen, plotBar=True):
    """
    Input: complex dataframe for a given jellyfish
    Output: plots the % of pulses that have changed relative to a bounded angle and a given sensatitivy as defined by centralizationFigure
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    if plotBar:
        # gridspec organization
        heights = [4, 1]
        gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

        # plot bar
        ax2 = fig.add_subplot(gs[1, 0])
        figures.bar4MovementDayNight(dfComplex, ax2)

        # save fig
        outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterChangedWithBar')
    else:
        # gridspec organization
        heights = [1]
        gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

        #save fig
        outpath = outdir / '{}_{}.png'.format(jelly_title, 'CenterChanged')

    ax1 = fig.add_subplot(gs[0, 0])
    figures.centralizationFigure(jelly_title, ax1, dfComplex)

    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plot_ganglia_centralization(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen, plotBar=True):
    """
    Input: complex dataframe for a given jellyfish
    Output: plots the % of pulses that have changed relative to a bounded angle and a given sensatitivy as defined by centralizationFigure
    """
    updateparameters()

    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    if plotBar:
        # gridspec organization
        heights = [4, 1]
        gs = fig.add_gridspec(ncols=1, nrows=2, height_ratios=heights)

        # plot bar
        ax2 = fig.add_subplot(gs[1, 0])
        figures.bar4MovementDayNight(dfComplex, ax2)

        # save fig
        outpath = outdir / '{}_{}.png'.format(jelly_title, 'GangliaChangedWithBar')
    else:
        # gridspec organization
        heights = [1]
        gs = fig.add_gridspec(ncols=1, nrows=1, height_ratios=heights)

        #save fig
        outpath = outdir / '{}_{}.png'.format(jelly_title, 'GangliaChanged')

    ax1 = fig.add_subplot(gs[0, 0])
    figures.ganglia_centralization(jelly_title, ax1, dfComplex)

    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def plotBar(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen):
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

    figures.bar4MovementDayNight(dfComplex, ax1)

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'plotBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def ActigramANDPulseRateWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen):
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

    figures.actigramFigure(dfActigram, dfComplex, ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels)
    figures.bar4MovementDayNight(dfComplex, ax2)
    figures.pulseRate(jelly_title, ax3, dfComplex, show_title=False, show_xLabels=False)

    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'ActigramANDPulseRate')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def Actigram_PR_CC_AND_CHVertWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen, hist_constraints=[]):
    """ input: complex dataframe for a jelly
    Output: figure displaying all of the plots from graphs of: Actigram, interpulse interval, centersChanged, and vertical
    CenterHistogram with the day/night bar"""

    updateparameters()
    # create empty figure with customized dimensions. "constrained_layout" automatically adjusts subplots to fit window
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization: fig has two columns, four large figures and several smaller supplementary figs.
    heights = [15, 1, 3, 3]
    widths = [10, 1]
    gs = fig.add_gridspec(ncols=2, nrows=4, height_ratios = heights, width_ratios = widths)

    # subplots - created and assigned to a graph below
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])
    fig_ax3 = fig.add_subplot(gs[2,0])
    fig_ax4 = fig.add_subplot(gs[3,0])
    fig_ax5 = fig.add_subplot(gs[0,1])

    figures.actigramFigure(dfActigram, dfComplex, fig_ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels)
    figures.bar4MovementDayNight(dfComplex,  fig_ax2)
    figures.pulseRate(jelly_title, fig_ax3, dfComplex, show_title=False, show_xLabels=False)
    figures.centralizationFigure(jelly_title, fig_ax4, dfComplex, show_title=False, show_xLabels=False, show_Legend=False)
    figures.initiatiorsHistogramFigure(jelly_title, fig_ax5, dfComplex, vertical=True, show_title=False, show_degreeLabels=False, constraints=hist_constraints)
    # individual titles, legends and labels are turned off
    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram_PR_CC_AND_CHVert')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def Actigram_PR_CC_AND_CHDayNightWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen, hist_constraints=[]):
    """
    input: complex dataframe for a jelly
    Output: figure displaying all of the plots from graphs of: Actigram, interpulse interval, centersChanged, and
    pulse initiation day-night Histogram with the day/night bar
    """

    updateparameters()

    # create empty figure with customized dimensions. "constrained_layout" automatically adjusts subplots to fit window
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization: 3 columns, 4 rows, with boxes of their respective size ratio
    heights = [15, 1, 5, 5]
    widths = [20, 1, 1]
    gs = fig.add_gridspec(ncols=3, nrows=4, height_ratios = heights, width_ratios = widths)

    # subplots  - created and assigned to a graph below
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])
    fig_ax3 = fig.add_subplot(gs[2,0])
    fig_ax4 = fig.add_subplot(gs[3,0])
    fig_ax5 = fig.add_subplot(gs[0,1])
    fig_ax6 = fig.add_subplot(gs[0,2])

    figures.actigramFigure(dfActigram, dfComplex, fig_ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels)
    figures.bar4MovementDayNight(dfComplex, fig_ax2)
    figures.pulseRate(jelly_title, fig_ax3, dfComplex, show_title=False, show_xLabels=False)
    figures.centralizationFigure(jelly_title, fig_ax4, dfComplex, show_title=False, show_xLabels=False, show_Legend=False)

    figures.initiatiorsHistogramFigure('Day', fig_ax5, dfComplex, rhopaliaPositions360, rhopaliaLabels, show_title=True, show_degreeLabels=False, constraints=hist_constraints, question='DayOrNight == \'Day\'')
    figures.initiatiorsHistogramFigure('Night', fig_ax6, dfComplex, rhopaliaPositions360, rhopaliaLabels, show_title=True, show_degreeLabels=False, constraints=hist_constraints, question='DayOrNight == \'Night\'')

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram_PR_CC_AND_CHDayNight')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def Actigram_PR_CC_DM_AND_CHDayNightWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopaliaPositions360, rhopaliaLabels, yfigurelen, xfigurelen, hist_constraints=[]):
    """
    input: complex dataframe for a jelly
    Output: figure displaying all of the plots from graphs of: Actigram, interpulse interval, centersChanged, and
    pulse initiation day-night Histogram with the day/night bar
    """

    updateparameters()

    # create empty figure with customized dimensions. "constrained_layout" automatically adjusts subplots to fit window
    fig = plt.figure(figsize=(xfigurelen, yfigurelen), constrained_layout=True)

    # gridspec organization: 3 columns, 4 rows, with boxes of their respective size ratio
    heights = [15, 1, 5, 5, 5]
    widths = [20, 1, 1]
    gs = fig.add_gridspec(ncols=3, nrows=5, height_ratios = heights, width_ratios = widths)

    # subplots  - created and assigned to a graph below
    fig_ax1 = fig.add_subplot(gs[0,0])
    fig_ax2 = fig.add_subplot(gs[1,0])
    fig_ax3 = fig.add_subplot(gs[2,0])
    fig_ax4 = fig.add_subplot(gs[3,0])
    fig_ax5 = fig.add_subplot(gs[4,0])
    fig_ax6 = fig.add_subplot(gs[0,1])
    fig_ax7 = fig.add_subplot(gs[0,2])

    figures.actigramFigure(dfActigram, dfComplex, fig_ax1, jelly_title, rhopaliaPositions360, rhopaliaLabels)
    figures.bar4MovementDayNight(dfComplex, fig_ax2)
    figures.pulseRate(jelly_title, fig_ax3, dfComplex, show_title=False, show_xLabels=False)
    figures.centralizationFigure(jelly_title, fig_ax4, dfComplex, show_title=False, show_xLabels=False, show_Legend=False)
    figures.distanceMoved(jelly_title, fig_ax5, dfComplex, show_title = False, show_xLabels=False)

    figures.initiatiorsHistogramFigure('Day', fig_ax6, dfComplex, rhopaliaPositions360, rhopaliaLabels, show_title=True, show_degreeLabels=False, constraints=hist_constraints, question='DayOrNight == \'Day\'')
    figures.initiatiorsHistogramFigure('Night', fig_ax7, dfComplex, rhopaliaPositions360, rhopaliaLabels, show_title=True, show_degreeLabels=False, constraints=hist_constraints, question='DayOrNight == \'Night\'')

    #save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'Actigram_PR_CC_DM_AND_CHDayNightWithBar')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


def anglesHistogramDayANDNightPlot(outdir, jelly_title, dfComplex, rhopos, rholab, yfigurelen, xfigurelen):
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

    figures.initiatiorsHistogramFigure('Day', fig_ax1, dfComplex, rhopos, rholab, vertical=False, show_title=True,
                                            show_degreeLabels=True, question='DayOrNight == \'Day\'')
    figures.initiatiorsHistogramFigure('Night', fig_ax2, dfComplex, rhopos, rholab, vertical=False, show_title=True,
                                            show_degreeLabels=True, question='DayOrNight == \'Night\'')

    fig.suptitle(jelly_title)

    #save fig
    # save fig
    outpath = outdir / '{}_{}.png'.format(jelly_title, 'anglesHistogramDayANDNightPlot')
    fig.savefig(str(outpath),bbox_inches='tight')

    plt.close()


##############################################################

##############################################################

##############################################################

def main(jelly_title, outdir, dfComplex, rhopos, rholab, stdYlen = None, stdXlen = None, Framerate=120, histogram_constraints=[]):
    """
    :param jelly_title: name of jellyfish
    :param outdir: output directory where png's will be saved
    :param dfComplex:complex DF
    :param RHOPOS:rhopalia position
    :param RHOLAB:rhopalia label
    :return:
    """

    dfActigram = cdf.createActigramArr(dfComplex, Framerate)

    #standard graph sizes
    if stdYlen is None: stdYlen = 15/2
    if stdXlen is None: stdXlen = dfComplex['AbsoluteMinute'].max()/60*5/3

    # with bar

    plotInterpulseInterval(outdir, jelly_title, dfComplex, stdYlen, stdXlen)

    plotPulseRate(outdir, jelly_title, dfComplex, stdYlen, stdXlen)

    plotAngleHistogramVertical(outdir, jelly_title, dfComplex, rhopos, rholab, 18, 5, hist_constraints = histogram_constraints)

    plotAngleHistogramHorizontal(outdir, jelly_title, dfComplex, rhopos, rholab, 5, 18, hist_constraints = histogram_constraints)

    plotDistanceMoved(outdir, jelly_title, dfComplex, stdYlen, stdXlen)

    plotCentralization(outdir, jelly_title, dfComplex, stdYlen, stdXlen)

    plotActigram(outdir, jelly_title, dfActigram, dfComplex, rhopos,rholab, stdYlen, stdXlen)

    plotBar(outdir, jelly_title, dfComplex, 2, stdXlen)

    # combined

    ActigramANDPulseRateWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopos,rholab, stdYlen+2, stdXlen)

    Actigram_PR_CC_AND_CHVertWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopos,rholab, stdYlen+8, stdXlen, hist_constraints = histogram_constraints)

    Actigram_PR_CC_AND_CHDayNightWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopos,rholab, stdYlen+8, stdXlen, hist_constraints = histogram_constraints)

    Actigram_PR_CC_DM_AND_CHDayNightWithBar(outdir, jelly_title, dfActigram, dfComplex, rhopos,rholab, stdYlen+11, stdXlen, hist_constraints = histogram_constraints)

    # histogram partitions

    anglesHistogramDayANDNightPlot(outdir, jelly_title, dfComplex, rhopos, rholab, 20, 36)

    plotHistorgram4DayLightSlices(outdir, jelly_title, dfComplex, rhopos, rholab, 5, 15, hist_constraints = histogram_constraints)

    plotHistorgram4DayHourSlices(outdir, jelly_title, dfComplex, rhopos, rholab, 5, 15, hist_constraints = histogram_constraints)

    # trajectory plotting

    plotJellyTrajectory(outdir, jelly_title, dfComplex)

    plotJellyTrajectoryDayNight(outdir, jelly_title, dfComplex)

    create_trajectory_gif(dfComplex, jelly_title, outdir)