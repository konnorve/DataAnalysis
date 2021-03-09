from pathlib import Path
import numpy as np
from datetime import datetime, timedelta, tzinfo
import DataFrameCreationMethods as cdf
import plottingMethods as pm
from re import search
import pytz
import pandas as pd

# datetime(year,month,day,strthr,strtmin) + timedelta(0, sec 0, 0, 0, min 0, hour 0),


rho_df_path = Path(r'I:\Ganglia_Tracker_Data\Rhopalia_Positions.csv')
rhopalia_positions = pd.read_csv(rho_df_path)


home_dir = Path(r'I:\Ganglia_Tracker_Data')

cumulative_complexDF_dir = cdf.makeOutDir(home_dir, 'complexDFs')

for jelly_dir in home_dir.iterdir():
    if jelly_dir.is_dir():

        jelly_name = jelly_dir.name
        print('\n' + jelly_name)

        rhopaliaDF = None

        rhopaliaDF = rhopalia_positions.loc[(rhopalia_positions['Jellyfish'] == jelly_name)]

        print(rhopaliaDF.head())

        for recording_dir in jelly_dir.iterdir():
            if recording_dir.is_dir():
                recording_name = recording_dir.name

                angle_dir = None
                orientation_path = None
                start_datetime = None
                isDaylightSavings = None

                dir_items = [x for x in recording_dir.iterdir()]

                print(dir_items)

                # getting angle dir and orientation csv
                for item in dir_items:
                    if search('AngleData', str(item)):
                        angle_dir = item
                    elif search('orientations', str(item)):
                        if search('.csv', str(item)):
                            orientation_path = item

                # getting start time and daylight savings bool

                fractions = recording_name.split('_')
                print(fractions)

                date = fractions[0]
                time = None
                for frac in fractions:
                    if search('(\d){3,4}am|pm', frac):
                            time = frac

                if time is not None:
                    if len(time) != 6:
                        time = '0' + time

                    string_datetime = date + ' ' + time

                    start_datetime = datetime.strptime(string_datetime, '%Y%m%d %I%M%p')

                    timezone = pytz.timezone('US/Pacific')

                    temp_time = timezone.localize(start_datetime)

                    isDaylightSavings = temp_time.dst() != timedelta(0)

                print(
                    'rec name: {} \t st: {} \t daylight savings?:{} \t angleDir found: {} \t orientation sheet found: {}'.format(
                        recording_name, start_datetime, isDaylightSavings, angle_dir is not None,
                        orientation_path is not None))

                item_list = [angle_dir, orientation_path, start_datetime, isDaylightSavings]

                if None not in item_list:
                    complexDF = cdf.createComplexDF(angleDataPath=angle_dir,
                                        orientationDF=pd.read_csv(orientation_path),
                                        rhopaliaDF=rhopaliaDF,
                                        FRAMERATE=120,
                                        STARTDATETIME=start_datetime,
                                        DAYLIGHTSAVINGS=isDaylightSavings)
                    """
                    complexDFPath1 = recording_dir / '{}_complexDF.csv'.format(recording_name)
                    complexDFPath2 = cumulative_complexDF_dir / '{}_complexDF.csv'.format(recording_name)

                    complexDF.to_csv(complexDFPath1)
                    complexDF.to_csv(complexDFPath2)
                    """

                    if False:
                        figures_path = cdf.makeOutDir(recording_dir, 'figures')

                        rhopos = rhopaliaDF['Rhopalia Position'].tolist()
                        rholab = rhopaliaDF['Rhopalia Label'].tolist()

                        pm.main(recording_name, figures_path, complexDF, rhopos, rholab, histogram_constraints=[0, 0.025])


