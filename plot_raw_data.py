import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvas
import matplotlib.gridspec as gridspec
import numpy as np

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


def plot_ly(lon,lat,alt,time,power,density,weight,bins,file_path,clear_fig,current_time_range,maps):
    '''Plotting routine to view raw data. Select map=False or True to view a 3 panel or single panel 
    plot of the raw lma data. All other kwargs are used to display specific user selected traits of the data,
    e.g. raw source locations, gridded source count densities, etc.
    '''
    fig = make_subplots(
        rows=5, cols=4,shared_xaxes=True,shared_yaxes=True,
        specs=[[{'colspan':3,"rowspan":2}, None, {},{}],
               [None,None,None,None],
               [{'colspan':3,"rowspan":3},{},{},{"rowspan":3}],
               [None,None,None,None],
               [None,None,None,None]],
#         print_grid=True
    )


    fig.update_layout(
        autosize=False,
        width=1000,
        height=900)
    
    if maps == True:
    
        if clear_fig == 'No Data Found':
            print('Nope')
            if density == 'Points' or density == 'Density':
                if weight is not None:
                    fig.add_trace(go.Scatter(x=[0,0,0],y=[0,0,0]),row=1,col=1)
                    fig.add_trace(go.Scatter(x=[0,0,0],y=[0,0,0]),row=3,col=4)
                    fig.add_trace(go.Scatter(x=[0,0,0],y=[0,0,0]),row=3,col=1)

        else:
            if density == 'Points':
                print('Picked Points')
                fig.add_trace(go.Scatter(x=[0,0,0],y=[0,0,0]),row=1,col=1)
                fig.add_trace(go.Scatter(x=[0,0,0],y=[0,0,0]),row=3,col=4)
                fig.add_trace(go.Scatter(x=[0,0,0],y=[0,0,0]),row=3,col=1)

                if weight == 'None':
                    fig.update_traces(go.Scatter(x=lon, y=alt,mode='markers',),
                                     row=1, col=1)

                    fig.update_traces(go.Scatter(x=lon, y=lat,mode='markers',),
                                     row=3, col=1)

                    fig.update_traces(go.Scatter(x=alt, y=lat,mode='markers',),
                                     row=3, col=4)
                else:
                    if weight == 'alt':
                        weight = alt/1e4
                        cmap = cm.cm.deep_r
                    elif weight == 'time':
                        weight = time/1e9
                        cmap   = plt.cm.magma
                    elif weight == 'power':
                        weight = power*3e1
                        cmap = cm.cm.algae_r


                    fig.update_traces(go.Scatter(x=lon, y=alt,mode='markers',marker=dict(size=weight,color='black')),
                                     row=1, col=1)

                    fig.update_traces(go.Scatter(x=lon, y=lat,mode='markers',marker=dict(size=weight,color='black')),
                                     row=3, col=1)

                    fig.update_traces(go.Scatter(x=alt, y=lat,mode='markers',marker=dict(size=weight,color='black')),
                                     row=3, col=4)

            else:
                h0xy,xe1,ye1 = np.histogram2d(lon,lat,bins=(int(bins),int(bins)))
                h0xz,xe2,ye2 = np.histogram2d(lon,alt,bins=(int(bins),int(bins)))
                h0yz,xe3,ye3 = np.histogram2d(alt,lat,bins=(int(bins),int(bins)))


                colors = fig.add_trace(go.Heatmap(z=h0xy.T,showscale=True,coloraxis='coloraxis'),row=3,col=1)
                fig.add_trace(go.Heatmap(z=h0xz.T,coloraxis='coloraxis'),row=1,col=1)
                fig.add_trace(go.Heatmap(z=h0yz.T,coloraxis='coloraxis'),row=3,col=4)


                if weight=='None':
                    cbar_title= r'LMA Sources per square km'

                    fig.update_traces(go.Heatmap(x=xe1,y=ye1,
                                            z=np.log10(h0xy).T,
                                            showscale=True,coloraxis='coloraxis'), row=3,col=1)

                    fig.update_traces(go.Heatmap(x=xe2,y=ye2,
                                            z=np.log10(h0xz).T,
                                            coloraxis='coloraxis'), row=1,col=1)

                    fig.update_traces(go.Heatmap(x=xe3,y=ye3,
                                            z=np.log10(h0yz).T,
                                            coloraxis='coloraxis'), row=3,col=4)

                    color_bar_pref = dict(
                                        title=cbar_title,
                                        thicknessmode="pixels", thickness=40,
                                        lenmode="pixels", len=600,
                                        yanchor="bottom", 
                                        y=0.05,
                                        )

                    fig.update_layout(coloraxis_colorbar=color_bar_pref,coloraxis = {'colorscale':'viridis'})


                else:
                    if weight == 'alt':
                        cbar_title = 'LMA Source Altitude'
                        weight = alt
                        cmap = cm.cm.deep_r
                    elif weight == 'time':
                        cbar_title = 'LMA Source Time'
                        weight = time
                        cmap   = plt.cm.magma
                    elif weight == 'power':
                        cbar_title = 'LMA Source Power'
                        weight = power
                        cmap = cm.cm.algae_r

                    h0xy0,xe1,ye1 = np.histogram2d(lon,lat,bins=(int(bins),int(bins)),weights=weight)
                    h0xz0,xe2,ye2 = np.histogram2d(lon,alt,bins=(int(bins),int(bins)),weights=weight)
                    h0yz0,xe3,ye3 = np.histogram2d(alt,lat,bins=(int(bins),int(bins)),weights=weight)

                    fig.update_traces(go.Heatmap(x=xe1,y=ye1,
                                            z=(h0xy0/h0xy).T,
                                            showscale=True,coloraxis='coloraxis'), row=3,col=1)

                    fig.update_traces(go.Heatmap(x=xe2,y=ye2,
                                            z=(h0xz0/h0xz).T,
                                            coloraxis='coloraxis'), row=1,col=1)

                    fig.update_traces(go.Heatmap(x=xe3,y=ye3,
                                            z=(h0yz0/h0yz).T,
                                            coloraxis='coloraxis'), row=3,col=4)

                    color_bar_pref = dict(
                                        title=cbar_title,
                                        thicknessmode="pixels", thickness=40,
                                        lenmode="pixels", len=600,
                                        yanchor="bottom", 
                                        y=0.05,
                                        )
                    fig.update_layout(coloraxis_colorbar=color_bar_pref,coloraxis = {'colorscale':'viridis'})


            fig.update_layout(showlegend=False, title_text=r"Date: {0}-{1}-{2} {3}".format(file_path.year,file_path.month,file_path.day,current_time_range))
            fig.update_xaxes(matches='x',row=1,col=1)
            fig.update_xaxes(matches='x',row=3,col=1)
            fig.update_yaxes(matches='y2',row=3,col=1)
            fig.update_yaxes(matches='y2',row=3,col=4)
            fig.update_yaxes(matches='y',row=1,col=1)
            fig.update_xaxes(matches='y',row=3,col=4)
        
        responsive = pn.pane.Plotly(fig, config={'responsive': True})
    else:
        #Original use of Plotl's MapBox
        #fig.add_trace(go.Densitymapbox(lon=lon, lat=lat,
        #                         radius=20))
        #fig.update_layout(mapbox_style="carto-positron",mapbox_center_lon=-101.5,mapbox_center_lat=34,mapbox=dict(zoom=6))
        #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
        #Switch to Holoviews for consistency:
        raw_hist,xe,ye = np.histogram2d(lon,lat,bins=(int(bins),int(bins)))

        # get xarray dataset, suited for handling raster data in pyviz
        xr_dataset = gv.Dataset(hv.Image((xe, ye, np.log10(np.ma.MaskedArray(raw_hist.T,mask=raw_hist.T==0))), bounds=(xe.min(),ye.min(),xe.max(),ye.max()), 
                kdims=[hv.Dimension('x'),  hv.Dimension('y')], datatype=['grid']))

        # create contours from image
        gv.FilledContours(xr_dataset)
        fig = gv.tile_sources.Wikipedia.opts(width=900, height=900) * xr_dataset.to.image(['x', 'y']).opts(cmap='cubehelix', alpha=0.8)#gv.FilledContours(xr_dataset).opts(cmap='viridis', alpha=0.5)
        responsive = pn.pane.HoloViews(fig, config={'responsive': True})
        
    return(responsive)