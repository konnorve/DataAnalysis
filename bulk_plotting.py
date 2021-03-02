from pathlib import Path
import numpy as np
from datetime import datetime, timedelta, tzinfo
import DataFrameCreationMethods as cdf
import plottingMethods as pm
from re import search
import pytz
import pandas as pd

# datetime(year,month,day,strthr,strtmin) + timedelta(0, sec 0, 0, 0, min 0, hour 0),


import sys



def plot_jelly(complexDF_path):

    home_dir = Path(r'/home/kve/Insync/kve_berk_gdrive/Bulk_plotting_Feb_27')

    rho_df_path = home_dir / 'Rhopalia_Positions.csv'
    rhopalia_positions = pd.read_csv(rho_df_path)

    if complexDF_path.suffix == ".csv":

        full_name = complexDF_path.name
        print('\n' + full_name)

        fractions = full_name.split('_')

        jelly_name = fractions[1]

        try:
            rhopaliaDF = rhopalia_positions.loc[(rhopalia_positions['Jellyfish'] == jelly_name)]

        except:
            rhopaliaDF = None

        recording_name = full_name[:full_name.find('_complexDF')]

        jelly_dir = cdf.makeOutDir(home_dir, jelly_name)

        recording_dir = cdf.makeOutDir(jelly_dir, recording_name)

        complexDF = pd.read_csv(complexDF_path)

        print(complexDF.head())

        figures_path = cdf.makeOutDir(recording_dir, 'figures')

        rhopos = rhopaliaDF['Rhopalia Position'].tolist()
        rholab = rhopaliaDF['Rhopalia Label'].tolist()

        pm.core(recording_name, figures_path, complexDF, rhopos, rholab, histogram_constraints=[0, 0.025])


if __name__ == "__main__":
    complex_df_path = Path(sys.argv[1])

    plot_jelly(Path(complex_df_path))