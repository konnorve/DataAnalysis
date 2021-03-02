#!/bin/bash

complex_df_folder=/home/kve/Insync/kve_berk_gdrive/Bulk_plotting_Feb_27/complexDFs/

for complex_df_path in $complex_df_folder/*
do
  python bulk_plotting.py $complex_df_path
done