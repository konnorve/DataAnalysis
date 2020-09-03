

import DataFrameCreationMethods as cdf
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import plottingMethods as pm
import matplotlib.cm as cm

#datetime(year,month,day,strthr,strtmin) + timedelta(0, sec 0, 0, 0, min 0, hour 0),



recordingTitle_P1 = '20200706_Pink_755pm_cam2_1'
angleDataPath_P1 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Pink_755pm_cam2_1/AngleData')
complexDFoutpath_P1 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Pink_755pm_cam2_1/ComplexDF/20200706_Pink_755pm_cam2_1_MichaelOrientation.csv')
figureOutDir_P1 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Pink_755pm_cam2_1/figures')
starttime_P1 = datetime(2020,7,6,19,55)
data_P1 = pd.DataFrame([[0, -85],
                      [1, -110],
                      [2, -140],
                      [3, -125],
                      [4, -137],
                      [5, -12],
                      [6, 25]], columns = ['movement segment', 'orientation factor'])

complexDF_P1 = cdf.createComplexDF(
            angleDataPath_P1,
            data_P1,
            120,
            starttime_P1,
            DAYLIGHTSAVINGS=True
            )
complexDF_P1.to_csv(str(complexDFoutpath_P1), index = False)



recordingTitle_P2 = '20200707_Pink_218pm_cam2_1'
angleDataPath_P2 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Pink_218pm_cam2_1/AngleData')
complexDFoutpath_P2 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Pink_218pm_cam2_1/ComplexDF/20200707_Pink_218pm_cam2_1_MichaelOrientation.csv')
figureOutDir_P2 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Pink_218pm_cam2_1/figures')
starttime_P2 = datetime(2020,7,7,14,18)
data_P2 = pd.DataFrame([[0, 27],
                      [1, -111],
                      [2, -115],
                      [3, -92],
                      [4, -53],
                      [5, -75],
                      [6, -54],
                      [7, -118],
                      [8, -21],
                      [9, -50],
                      [10, -89],
                      [11, -88],
                      [12, -65],
                      [13, -44],
                      [14, 30]], columns = ['movement segment', 'orientation factor'])

complexDF_P2 = cdf.createComplexDF(
            angleDataPath_P2,
            data_P2,
            120,
            starttime_P2,
            DAYLIGHTSAVINGS=True
            )
complexDF_P2.to_csv(str(complexDFoutpath_P2), index = False)




complexDF_Pconcat = cdf.dfConcatenator(complexDF_P1, starttime_P1, complexDF_P2, starttime_P2)
complexDFoutpath_Pconcat = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/Pink_concatDF_2020706-7/ComplexDF/Pink_concatDF_2020706-7_MichaelOrientation.csv')
complexDF_Pconcat.to_csv(str(complexDFoutpath_Pconcat), index = False)

xticks_Pconcat = cdf.getXtickDF(complexDF_Pconcat)
actigramArr_Pconcat = cdf.createActigramArr(complexDF_Pconcat, 120, pulseExtension=1)
barArr_Pconcat = cdf.createDayNightMovementBar(complexDF_Pconcat)

recordingTitle_Pconcat = 'Pink_concatDF_2020706-7'
figureOutDir_Pconcat = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/Pink_concatDF_2020706-7/figures')

# pm.plotSensativity(figureOutDir_Pconcat, recordingTitle_Pconcat, complexDF_Pconcat, xticks_Pconcat, 7, complexDF_Pconcat['AbsoluteMinute'].max()/60*5/3)

pm.main(recordingTitle_Pconcat, figureOutDir_Pconcat, actigramArr_Pconcat, barArr_Pconcat, xticks_Pconcat, complexDF_Pconcat, [], [])


xticks_P1 = cdf.getXtickDF(complexDF_P1)
actigramArr_P1 = cdf.createActigramArr(complexDF_P1, 120, pulseExtension=1)
barArr_P1 = cdf.createDayNightMovementBar(complexDF_P1)

pm.main(recordingTitle_P1, figureOutDir_P1, actigramArr_P1, barArr_P1, xticks_P1, complexDF_P1, [], [])

xticks_P2 = cdf.getXtickDF(complexDF_P2)
actigramArr_P2 = cdf.createActigramArr(complexDF_P2, 120, pulseExtension=1)
barArr_P2 = cdf.createDayNightMovementBar(complexDF_P2)

pm.main(recordingTitle_P2, figureOutDir_P2, actigramArr_P2, barArr_P2, xticks_P2, complexDF_P2, [], [])


# recordingTitle_B1 = '20200706_Beyonce_755pm_cam1_1'
# angleDataPath_B1 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Beyonce_755pm_cam1_1/AngleData')
# complexDFoutpath_B1 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Beyonce_755pm_cam1_1/ComplexDF/20200706_Beyonce_755pm_cam1_1_MichaelOrientation.csv')
# figureOutDir_B1 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Beyonce_755pm_cam1_1/figures')
# starttime_B1 = datetime(2020,7,6,19,55)
# data_B1 = pd.DataFrame([[0, 75],
#                       [1, 57],
#                       [2, 56],
#                       [3, 49],
#                       [4, 49],
#                       [5, 105],
#                       [6, -168],
#                       [7, 168],
#                       [8, -48],
#                       [9, -29],
#                       [10, -83],
#                       [11, -115]], columns = ['movement segment', 'orientation factor'])
#
# complexDF_B1 = cdf.createComplexDF(
#             angleDataPath_B1,
#             data_B1,
#             120,
#             starttime_B1,
#             DAYLIGHTSAVINGS=True
#             )
# complexDF_B1.to_csv(str(complexDFoutpath_B1), index = False)
#
# recordingTitle_B2 = '20200707_Beyonce_219pm_cam1_1'
# angleDataPath_B2 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Beyonce_219pm_cam1_1/AngleData')
# complexDFoutpath_B2 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Beyonce_219pm_cam1_1/ComplexDF/20200707_Beyonce_219pm_cam1_1_MichaelOrientation.csv')
# figureOutDir_B2 = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Beyonce_219pm_cam1_1/figures')
# starttime_B2 = datetime(2020,7,7,14,19)
# data_B2 = pd.DataFrame([[0, -117],
#                       [1, -156],
#                       [2, 164],
#                       [3, -159],
#                       [4, -137],
#                       [5, -117],
#                       [6, np.nan],
#                       [7, 162],
#                       [8, 108],
#                       [9, 84],
#                       [10, -141]], columns = ['movement segment', 'orientation factor'])
#
# complexDF_B2 = cdf.createComplexDF(
#             angleDataPath_B2,
#             data_B2,
#             120,
#             starttime_B2,
#             DAYLIGHTSAVINGS=True
#             )
# complexDF_B2.to_csv(str(complexDFoutpath_B2), index = False)
#
#
#
#
# compledDF_Bconcat = cdf.dfConcatenator(complexDF_B1, starttime_B1, complexDF_B2, starttime_B2)
# complexDFoutpath_Bconcat = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/Beyonce_concatDF_2020706-7/ComplexDF/Beyonce_concatDF_2020706-7_MichaelOrientation.csv')
# compledDF_Bconcat.to_csv(str(complexDFoutpath_Bconcat), index = False)
#
# xticks_Bconcat = cdf.getXtickDF(compledDF_Bconcat)
# actigramArr_Bconcat = cdf.createActigramArr(compledDF_Bconcat, 120, pulseExtension=1)
# barArr_Bconcat = cdf.createDayNightMovementBar(compledDF_Bconcat)
#
# recordingTitle_Bconcat = 'Beyonce_concatDF_2020706-7'
# figureOutDir_Bconcat = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/Beyonce_concatDF_2020706-7/figures')
#
# pm.main(recordingTitle_Bconcat, figureOutDir_Bconcat, actigramArr_Bconcat, barArr_Bconcat, xticks_Bconcat, compledDF_Bconcat, [], [])
#
#
# xticks_B1 = cdf.getXtickDF(complexDF_B1)
# actigramArr_B1 = cdf.createActigramArr(complexDF_B1, 120, pulseExtension=1)
# barArr_B1 = cdf.createDayNightMovementBar(complexDF_B1)
#
# pm.main(recordingTitle_B1, figureOutDir_B1, actigramArr_B1, barArr_B1, xticks_B1, complexDF_B1, [], [])
#
# xticks_B2 = cdf.getXtickDF(complexDF_B2)
# actigramArr_B2 = cdf.createActigramArr(complexDF_B2, 120, pulseExtension=1)
# barArr_B2 = cdf.createDayNightMovementBar(complexDF_B2)
#
# pm.main(recordingTitle_B2, figureOutDir_B2, actigramArr_B2, barArr_B2, xticks_B2, complexDF_B2, [], [])





stdYlen = 15
stdXlen = 18*5



# pm.plotBar(figureOutDir, recordingTitle, barArr, 10, stdXlen)
# pm.plotBinaryActigramWithBar(figureOutDir, recordingTitle, actigramArr, barArr, xticks, [], [], stdYlen, stdXlen)
# pm.plotInterpulseIntervalWithBar(figureOutDir, recordingTitle, complexDF, barArr, stdYlen, stdXlen)



#
# actigramOutdir = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Beyonce_755pm_cam1_1/Figures/Actigrams')
#
# colormaps = [cm.bone, cm.gray, cm.gist_yarg, cm.gist_gray, cm.cividis, cm.binary, cm.GnBu]
#
#
# for colormap in colormaps:
#     actigramOutpath = actigramOutdir / '20200706_Beyonce_755pm_cam1_1_{}_actigram.png'.format(colormap.name)
#     pm.plotCenters(actigramOutpath, 'beyonce cm: {}'.format(colormap.name), actigramCSV, xticks, [], [], 10, 18*5, colormap)

#
# outpath4actigramCSV = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200706_Beyonce_755pm_cam1_1/ComplexDF/20200706_Beyonce_755pm_cam1_1_actigram.csv')
# actigramCSVarr = cdf.createActigramCSV(complexDF, 120).T
