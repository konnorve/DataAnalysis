from pathlib import Path
import numpy as np
from datetime import datetime, timedelta, tzinfo
import DataFrameCreationMethods as cdf
import plottingMethods as pm
from re import search
import pytz
import pandas as pd

home_dir = Path('/home/kve/Desktop/Labora/Harland_Lab/2021-04/Bulk_Plotting_20210428/')
concatDF_path = home_dir / 'concatComplexDF.csv'
rho_df_path = home_dir / 'Rhopalia_Positions.csv'

rhopalia_positions = pd.read_csv(rho_df_path)

concat_figures_dir = cdf.makeOutDir(home_dir, 'concat_figures')

concatDF = pd.read_csv(concatDF_path)

unique_jellies = concatDF.Jellyfish.unique()

for jelly in unique_jellies:
    print(jelly)
    # if not (jelly in ['Lgaga', 'Beyonce', 'Janis']):
    complexDF = concatDF[concatDF['Jellyfish']==jelly]

    rhopaliaDF = rhopalia_positions.loc[(rhopalia_positions['Jellyfish'] == jelly)]

    concat_jelly_dir = cdf.makeOutDir(concat_figures_dir, jelly)

    rhopos = rhopaliaDF['Rhopalia Position'].tolist()
    rholab = rhopaliaDF['Rhopalia Label'].tolist()

    pm.core(jelly, concat_jelly_dir, complexDF, rhopos, rholab, histogram_constraints=[0, 0.05])