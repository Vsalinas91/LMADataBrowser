import xarray as xr
import pandas as pd
import numpy as np

import gzip
import datetime as dt
import glob as gl
import calendar

import pyxlma.lmalib.io.read as pyread
from flash_sort_and_grid import sort_grid
from panel.widgets.indicators import BooleanStatus, LoadingSpinner
import panel as pn

from plot_raw_data import plot_ly
from plot_gridded_data import plot_grids

spinner = LoadingSpinner(width=25,height=25)


def date_to_path(date):
    get_date = date
    year      = str(get_date.year)
    month_int = get_date.month
    month_abb = calendar.month_abbr[month_int]
    day       = str(get_date.day).zfill(2)
    file_path = f'Data/{year}/{month_abb}/{day}/*dat.gz'
    path = f'Data/{year}/{month_abb}/{day}/*'
    return(path)


def get_group(group,freq,grid_data,density=False,weight=False,bins=False,get_date=None,maps=True,process=False,view_processed=False,fields=False,plot_type=False,view_fn=plot_ly):
    '''This function is called when a specific date-time is selected to view any processed data. The file path determines 
    what data is loaded, and if no such path/data exists - the data will not be displayed. Many of the gui widget values for
    the processed data visualizations are kwargs, and are used to determine if the plot is mapped or paneled, and how the data are viewed,
    i.e. gridded or source points.
    
    FILL IN MORE DETAIL----
    '''
    #Initialize Event:
    #-------------
    year      = str(get_date.year)
    month_int = get_date.month
    month_abb = calendar.month_abbr[month_int]
    day       = str(get_date.day).zfill(2)
    file_path = f'Data/{year}/{month_abb}/{day}/*dat.gz'
    
    try:
        lma_files = [f for f in sorted(gl.glob(file_path))]
        lma_data = pyread.dataset(lma_files)
        pn.state.sync_busy(spinner)
        clear_fig = 'Data Found'

        #Event Data ALL DATA:
        #-----------
        times = lma_data[0].variables['event_time']
        tframe = int((times.values.max()-times.values.min())*1e-9 / 60)

        freqs       = freq#'120s'
        time_bins   = pd.date_range(times.min().values,times.max().values,freq=freqs)
        time_binsdt = time_bins.copy()
        time_bins   = time_bins.to_numpy()
        lma_data[0]['time_groups'] = xr.DataArray((np.digitize(times.values.view('i8'),time_bins.view('i8'))),dims='number_of_events')
        data_groups = list(lma_data[0].groupby('time_groups'))    

        #Dictionary for time bins
        dicts = {}
        starts = time_binsdt[:-1]
        ends   = time_binsdt[1:] 
        keys = np.arange(len(starts))
        for i in keys:
                dicts[i] = ("%s:%s") % (str(starts[i].hour).zfill(2), str(starts[i].minute).zfill(2)) + '-' + ("%s:%s UTC [HH:MM]") % ((str(ends[i].hour).zfill(2), str(ends[i].minute).zfill(2)))

        current_time_range = dicts[group]

        lon   = data_groups[group][1].variables['event_longitude']
        lat   = data_groups[group][1].variables['event_latitude']
        alt   = data_groups[group][1].variables['event_altitude']
        time  = data_groups[group][1].variables['event_time']
        power = data_groups[group][1].variables['event_power']

        time_stamps = (time.values.astype(dt.datetime) * 1e-9).astype(float)

        mask_alts = (alt<=30e3)
        
        
    except:
        freq = freq
        pn.state.sync_busy(spinner)
        clear_fig = 'No Data Found'
        lon = np.repeat(0,100)
        lat = np.repeat(0,100)
        alt = np.repeat(0,100)
        mask_alts = (alt<100)
        time_stamps = np.repeat(0,100)
        power = np.repeat(0,100)
        current_time_range = 0
    
    if view_processed == False:
        view_fn = plot_ly
        return(view_fn(lon[mask_alts],lat[mask_alts],alt[mask_alts],time_stamps[mask_alts],power[mask_alts],density,weight,bins,get_date,clear_fig,current_time_range,maps))
    elif view_processed == True:
        view_fn = plot_grids
        return(view_fn(grid_data,fields,plot_type))


