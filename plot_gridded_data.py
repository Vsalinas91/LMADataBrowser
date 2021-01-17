import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvas
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import cmocean as cm
import panel as pn

import holoviews as hv
import geoviews as gv
import geoviews.feature as gf
from cartopy import crs
from cartopy import feature as cf
from geoviews import opts
hv.extension('bokeh')
gv.extension('bokeh', 'matplotlib')


def plot_grids(data,fields,plot_type):
    if len(data) == 2: 
        ds,grid_ds = data
        
        if fields == 'Sources':
            print('Plotting Sources..')
            event_times_seconds = xr.DataArray(ds.event_time.values.astype('<m8[s]')/86400,dims='number_of_events')
            event_times_seconds.shape,ds.event_time.shape
            dss = ds.copy()
            dss['times'] = event_times_seconds.astype(int)

            xr_dataset = gv.Dataset(hv.Points((dss.event_longitude.values, dss.event_latitude.values,dss.times.values), 
                kdims=[hv.Dimension('x'),hv.Dimension('y')],vdims=['time']))

            fig = gv.tile_sources.Wikipedia.opts(width=900, height=900) * xr_dataset.to.points(['x','y']).opts(opts.Points(color='time'))

        else:
            print(plot_type)
            z = grid_ds.flash_extent_density
            x = grid_ds.grid_longitude.values
            y = grid_ds.grid_latitude.values

            # get xarray dataset, suited for handling raster data in pyviz
            xr_dataset = gv.Dataset(hv.Image((x, y, np.log10(z.mean(axis=0))), bounds=(x.min(),y.min(),x.max(),y.max()), 
                    kdims=[hv.Dimension('x'),  hv.Dimension('y')], datatype=['grid']))

            # create contours from image
            gv.FilledContours(xr_dataset)
            fig = gv.tile_sources.Wikipedia.opts(width=900, height=900) * xr_dataset.to.image(['x', 'y']).opts(cmap='cubehelix', alpha=0.8)#gv.FilledContours(xr_dataset).opts(cmap='viridis', alpha=0.5)


        responsive = pn.pane.HoloViews(fig, config={'responsive': True})
        return(responsive)
    
    else:
        grid_ds = data
        print('No Data Processed')
        if fields == 'Sources':
            xr_dataset = gv.Dataset(hv.Points((np.repeat(-101.1,1), np.repeat(32,2),np.repeat(10,2)), 
                kdims=[hv.Dimension('x'),hv.Dimension('y')],vdims=['time']))

            fig = gv.tile_sources.Wikipedia.opts(width=900, height=900) * xr_dataset.to.points(['x','y']).opts(opts.Points(color='time'))

        elif plot_type == 'Grids':
            z = np.random.randn(10,(100,100))
            x = np.repeat(-101.1,100) 
            y = np.repeat(32,100)
            
           

            # get xarray dataset, suited for handling raster data in pyviz
            xr_dataset = gv.Dataset(hv.Image((x, y, np.log10(z)), bounds=(x.min(),y.min(),x.max(),y.max()), 
                    kdims=[hv.Dimension('x'),  hv.Dimension('y')], datatype=['grid']))

            # create contours from image
            gv.FilledContours(xr_dataset)
            fig = gv.tile_sources.Wikipedia.opts(width=900, height=900) * xr_dataset.to.image(['x', 'y']).opts(cmap='cubehelix', alpha=0.8)#gv.FilledContours(xr_dataset).opts(cmap='viridis', alpha=0.5)


        responsive = pn.pane.HoloViews(fig, config={'responsive': True})
        return(responsive)
        

