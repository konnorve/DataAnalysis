# test

#update imports
# imports

import DataFrameCreationMethods as cdf
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import plottingMethods as pm
import matplotlib.cm as cm

#datetime(year,month,day,strthr,strtmin) + timedelta(0, sec 0, 0, 0, min 0, hour 0),

def makeOutDir(outputDir, folderName):
    outdir = outputDir / folderName
    if not outdir.exists():
        outdir.mkdir()
    return outdir

# Main input variables needed for DataFrame and Figures Creation

angleDataPath = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_10/Short_Behavioral_Recordings/Home/NinaSimone/NinaSimone_AngleData')
figureOutDir = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_10/Short_Behavioral_Recordings/Home/NinaSimone/Figures/')
starttime = datetime(2000,1,1,0,0)
orientationData = pd.read_csv(Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_10/Short_Behavioral_Recordings/Home/NinaSimone/NinaSimoneBehavioralTesting_OrientationFactors_completed_v2.csv'))
complexDFiofile= Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_10/Short_Behavioral_Recordings/Home/NinaSimone/ComplexDF/NinaSimoneComplexDF.csv')

complexDF = cdf.createComplexDF(angleDataPath, orientationData, 120, starttime, True)

complexDF = complexDF.loc[complexDF['chunk name']!='202001002_NinaSimone_335pm_Long_baseline']

complexDF.to_csv(str(complexDFiofile))

# complexDF = pd.read_csv(complexDFiofile)

uniqueChunks = complexDF['chunk name'].unique()

# complexDF_B1 = complexDF_B1.loc[(complexDF_B1['ZeitgeberDay']==7) & (complexDF_B1['ZeitgeberHour']==(5 or 6))]

for chunkName in uniqueChunks:
    complexDFslice = complexDF.loc[complexDF['chunk name']==chunkName]

    print(complexDFslice['chunk name'].unique())

    chunkFiguresOutDir = makeOutDir(figureOutDir, chunkName)

    xticks_P2 = cdf.getXtickDF(complexDFslice)

    actigramArr_P2 = cdf.createActigramArr(complexDFslice, 120, pulseExtension=1)

    barArr_P2 = cdf.createDayNightMovementBar(complexDFslice)

    pm.main(chunkName, chunkFiguresOutDir, actigramArr_P2, barArr_P2, xticks_P2, complexDFslice, [], [], stdXlen=15)

