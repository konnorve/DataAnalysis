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

homePath = Path('/Users/kve/Desktop/Clubs/Harland_Lab/Round_11/Lgaga/')

rec1path = homePath / '20200720_Lgaga_604pm_cam2_1'

rec1name = '20200720_Lgaga_604pm'

rec1FigureOutDir = makeOutDir(rec1path, 'Figures')

rec1ComplexDFOutpath = makeOutDir(rec1path, 'ComplexDF') / '{}_complexDF.csv'.format(rec1path.name)

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

complexDF1 = pd.read_csv(rec1ComplexDFOutpath)

pm.main(rec1name, rec1FigureOutDir, complexDF1, rhopos, rholab)

