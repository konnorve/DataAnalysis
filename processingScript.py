from pathlib import Path
import numpy as np
from datetime import datetime, timedelta, tzinfo
import DataFrameCreationMethods as cdf
import plottingMethods as pm
from re import search
import pytz

# datetime(year,month,day,strthr,strtmin) + timedelta(0, sec 0, 0, 0, min 0, hour 0),


# rho_df_path
home_dir = Path('/home/kve/Desktop/Labora/Harland_Lab/2021-2/Practice_with_multiprocessing')

for jelly_dir in home_dir.iterdir():
    if jelly_dir.is_dir():
        print('\n' + jelly_dir.name)
        for recording_dir in jelly_dir.iterdir():
            if recording_dir.is_dir():
                recording_name = recording_dir.name

                angle_dir = None
                orientation_path = None
                start_datetime = None
                isDaylightSavings = None

                dir_items = [x for x in recording_dir.iterdir()]

                # getting angle dir and orientation csv
                for item in dir_items:
                    if search('AngleData', str(item)):
                        angle_dir = item
                    elif search('orientations', str(item)):
                        if search('.csv', str(item)):
                            orientation_path = item

                # getting start time and daylight savings bool
                fractions = recording_name.split('_')

                if len(fractions[2]) != 6:
                    fractions[2] = '0' + fractions[2]

                string_datetime = fractions[0] + " " + fractions[2]
                start_datetime = datetime.strptime(string_datetime, '%Y%m%d %I%M%p')

                timezone = pytz.timezone('US/Pacific')

                start_datetime = timezone.localize(start_datetime)

                isDaylightSavings = start_datetime.dst() != timedelta(0)

                print(
                    'rec name: {} \t st: {} \t daylight savings?:{} \t angleDir found: {} \t orientation sheet found: {}'.format(
                        recording_name, start_datetime, isDaylightSavings, angle_dir is not None,
                        orientation_path is not None))

