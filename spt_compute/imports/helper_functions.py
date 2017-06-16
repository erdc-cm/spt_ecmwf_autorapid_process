# -*- coding: utf-8 -*-
##
##  helper_functions.py
##  spt_compute
##
##  Created by Alan D. Snow.
##  Copyright © 2015-2016 Alan D Snow. All rights reserved.
##  License: BSD-3 Clause

import datetime
from glob import glob
from netCDF4 import Dataset, num2date  # http://unidata.github.io/netcdf4-python/
import os
import re
from shutil import rmtree
import sys


#----------------------------------------------------------------------------------------
# HELPER FUNCTIONS
#----------------------------------------------------------------------------------------
class CaptureStdOutToLog(object):
    def __init__(self, out_file_path):
        self.out_file_path = out_file_path
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = sys.stderr = open(self.out_file_path, 'w')
        return self
    def __exit__(self, *args):
        sys.stdout.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr


def case_insensitive_file_search(directory, pattern):
    """
    Looks for file with pattern with case insensitive search
    """
    try:
        return os.path.join(directory,
                            [filename for filename in os.listdir(directory) \
                             if re.search(pattern, filename, re.IGNORECASE)][0])
    except IndexError:
        print("{0} not found".format(pattern))
        raise


def clean_main_logs(main_log_directory, prepend="spt_compute_ecmwf_",
                    lock_file_name="spt_compute_ecmwf_run_info_lock.txt"):
    """
    Removes old log files older than one week old in main log directory
    """
    date_today = datetime.datetime.utcnow()
    week_timedelta = datetime.timedelta(7)
    main_log_files = [f for f in os.listdir(main_log_directory) if
                      not os.path.isdir(os.path.join(main_log_directory, f))
                      and not log_file_path.endswith(f)
                      and f != lock_file_name]

    for main_log_file in main_log_files:
        try:
            log_datetime = datetime.datetime.strptime(main_log_file, "{0}%y%m%d%H%M%S.log".format(prepend))
            if (date_today-log_datetime > week_timedelta):
                os.remove(os.path.join(main_log_directory, main_log_file))
        except Exception as ex:
            print(ex)
            pass


def clean_logs(condor_log_directory, main_log_directory, prepend="spt_compute_ecmwf_", log_file_path=""):
    """
    This removed logs older than one week old
    """
    date_today = datetime.datetime.utcnow()
    week_timedelta = datetime.timedelta(7)
    #clean up condor logs
    condor_dirs = [d for d in os.listdir(condor_log_directory) if
                   os.path.isdir(os.path.join(condor_log_directory, d))]

    for condor_dir in condor_dirs:
        try:
            dir_datetime = datetime.datetime.strptime(condor_dir[:11], "%Y%m%d.%H")
            if (date_today-dir_datetime > week_timedelta):
                rmtree(os.path.join(condor_log_directory, condor_dir))
        except Exception as ex:
            print(ex)
            pass

    clean_main_logs(main_log_directory, prepend)


def find_current_rapid_output(forecast_directory, watershed, subbasin):
    """
    Finds the most current files output from RAPID
    """
    if os.path.exists(forecast_directory):
        basin_files = glob(os.path.join(forecast_directory,"Qout_%s_%s_*.nc" % (watershed, subbasin)))
        if len(basin_files) >0:
            return basin_files
    #there are none found
    return None


def get_valid_watershed_list(input_directory):
    """
    Get a list of folders formatted correctly for watershed-subbasin
    """
    valid_input_directories = []
    for directory in os.listdir(input_directory):
        if os.path.isdir(os.path.join(input_directory, directory)) \
            and len(directory.split("-")) == 2:
            valid_input_directories.append(directory)
        else:
            print("{0} incorrectly formatted. Skipping ...".format(directory))
    return valid_input_directories


def get_date_timestep_from_forecast_folder(forecast_folder):
    """
    Gets the datetimestep from forecast
    """
    #OLD: Runoff.20151112.00.netcdf.tar.gz
    #NEW: Runoff.20160209.0.exp69.Fgrid.netcdf.tar
    forecast_split = os.path.basename(forecast_folder).split(".")
    forecast_date_timestep = ".".join(forecast_split[1:3])
    return re.sub("[^\d.]+", "", forecast_date_timestep)


def get_date_range_from_qout_forecast(forecast_file):
    """
    Returns the string of time from the forecast file
    From: http://forum.marine.copernicus.eu/discussion/274/how-to-convert-netcdf-time-to-python-datetime-resolved/p1
    """
    file_in = Dataset(forecast_file)

    nctime = file_in.variables['time'][:]  # get values
    t_unit = file_in.variables['time'].units  # get unit  "days since 1950-01-01T00:00:00Z"

    try:
        t_cal = file_in.variables['time'].calendar
    except AttributeError:  # Attribute doesn't exist
        t_cal = u"gregorian"  # or standard

    file_in.close()

    dates = num2date(nctime, units=t_unit, calendar=t_cal)
    return "{start_datetime:%Y%m%d%H}to{end_datetime:%Y%m%d%H}".format(start_datetime=dates[0],
                                                                       end_datetime=dates[-1])

def get_date_range_from_lsm_files(path_to_lsm_files):
    """
    Retrieve date range from LSM files
    """

def get_ensemble_number_from_forecast(forecast_name):
    """
    Gets the datetimestep from forecast
    """
    #OLD: 20151112.00.1.205.runoff.grib.runoff.netcdf
    #NEW: 52.Runoff.nc
    forecast_split = os.path.basename(forecast_name).split(".")
    if forecast_name.endswith(".205.runoff.grib.runoff.netcdf"):
        ensemble_number = int(forecast_split[2])
    else:
        ensemble_number = int(forecast_split[0])
    return ensemble_number


def get_watershed_subbasin_from_folder(folder_name):
    """
    Get's the watershed & subbasin name from folder
    """
    input_folder_split = folder_name.split("-")
    watershed = input_folder_split[0].lower()
    subbasin = input_folder_split[1].lower()
    return watershed, subbasin


def log(message, severity):
    """Logs, prints, or raises a message.

    Arguments:
        message -- message to report
        severity -- string of one of these values:
            CRITICAL|ERROR|WARNING|INFO|DEBUG
    """

    print_me = ['WARNING', 'INFO', 'DEBUG']
    if severity in print_me:
        print("{0} {1}".format(severity, message))
    else:
        raise Exception(message)
