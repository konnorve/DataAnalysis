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
import figures as fig

#datetime(year,month,day,strthr,strtmin) + timedelta(0, sec 0, 0, 0, min 0, hour 0),

def makeOutDir(outputDir, folderName):
    outdir = outputDir / folderName
    if not outdir.exists():
        outdir.mkdir()
    return outdir

# Main input variables needed for DataFrame and Figures Creation

homePath = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_11.nosync/Lgaga/')

recPath = homePath / '20200723_Lgaga_730pm_cam2_1'

anglePath = recPath / '20200723_Lgaga_730pm_cam2_1_AngleData'

orientationDataPath = recPath / '20200723_Lgaga_730pm_cam2_1_Orientations_complete.csv'

rec1name = '20200723_Lgaga_730pm'

rec1FigureOutDir = makeOutDir(recPath, 'Figures')

rec1ComplexDFOutpath = makeOutDir(recPath, 'ComplexDF') / '{}_complexDF.csv'.format(recPath.name)

orientationDF = pd.read_csv(orientationDataPath)


complexDF = cdf.createComplexDF(anglePath,
                    orientationDF,
                    120,
                    datetime(2020,7,23,19,30),
                    True)

rhopos = [
            0.235,
            22.793,
            41.683,
            66.113,
            90.779,
            115.661,
            158.434,
            173.705,
            195.154,
            221.856,
            245.933,
            276.389,
            298.178,
            315.139,
            335.997,
        ]

rholab = list(range(1, len(rhopos)+1))

complexDF.to_csv(rec1ComplexDFOutpath)

complexDF = pd.read_csv(rec1ComplexDFOutpath)

pm.main(rec1name, rec1FigureOutDir, complexDF, rhopos, rholab)

