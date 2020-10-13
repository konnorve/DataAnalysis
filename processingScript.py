# test

# imports
import DataFrameCreationMethods as cdf
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import plottingMethods as pm
import matplotlib.cm as cm

#datetime(year,month,day,strthr,strtmin) + timedelta(0, sec 0, 0, 0, min 0, hour 0),

# Main input variables needed for DataFrame and Figures Creation
trainingTitle = '20200707_Pink_218pm_cam2_1'
angleDataPath = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Pink_218pm_cam2_1/AngleData')
complexDFoutpath = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Pink_218pm_cam2_1/ComplexDF/20200707_Pink_218pm_cam2_1_MichaelOrientation.csv')
figureOutDir = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_9/testdata4dataprocessingscript/20200707_Pink_218pm_cam2_1/figures')
starttime = datetime(2020,7,7,14,18)
data = pd.DataFrame([[0, 27],
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

complexDF = cdf.createComplexDF(
            angleDataPath,
            data,
            120,
            starttime,
            DAYLIGHTSAVINGS=True
            )

complexDF.to_csv(str(complexDFoutpath), index = False)

xticks_P2 = cdf.getXtickDF(complexDF)

print(xticks_P2)

actigramArr_P2 = cdf.createActigramArr(complexDF, 120, pulseExtension=1)

print(actigramArr_P2[:15])

barArr_P2 = cdf.createDayNightMovementBar(complexDF)

print(barArr_P2[:15])

pm.main(trainingTitle, figureOutDir, actigramArr_P2, barArr_P2, xticks_P2, complexDF, [], [])
