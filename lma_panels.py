import panel as pn
import panel.widgets as pnw
import param

import glob as gl
import datetime as dt
from read_data import get_group, date_to_path
from flash_sort_and_grid import sort_grid, fake_grid


from panel.widgets.indicators import LoadingSpinner
spinner = LoadingSpinner(width=25,height=25)



class LMAData(param.Parameterized):
    #RAW DATA
    get_date   = param.Date(dt.datetime(2019,5,26))
    time_step= param.String(default='60s')
    time_window  = param.Integer(default=0)#, bounds=(0, 9))
    density    = param.Selector(default='Density',objects=('Points','Density'))
    weight     = param.String(default='None')
    bins       = param.String(default='500')
    maps       = param.Boolean(default = None)

    
    #PROCESS:
    select_file  = param.Selector(default='')
    file_selected= param.String('Empty')
    process      = param.Boolean(default=None)
    view_processed=param.Boolean(constant=True)
    fields       = param.Selector(objects=('Sources','Grids'),constant=True)
    grids        = param.Selector(objects=('Flash Extent Density',
                                           'Mean Flash Area','Min Flash Area','Flash Size Std'),constant=True)
    
        
    @param.depends('get_date',watch=True) 
    def update_list(self):
        '''https://stackoverflow.com/questions/57870870/how-do-i-automatically-update-a-dropdown-selection-widget-when-another-selection'''
        path = date_to_path(self.get_date)
        files = [f for f in sorted(gl.glob(path))]
        if len(files) == 0:
            self.param['select_file'].objects = 'NONE'
        else:
            self.param['select_file'].objects = files
            
    @param.depends('select_file','process',watch=True)
    def process_data(self):
        file  = self.select_file
        self.file_selected = file[-32:-7]        
        if self.process == True:
            print('Starting flash sort and grid')
            try:
                self.data = sort_grid(file)
            except:
                print('Error in Flash Sorting')
            pn.state.sync_busy(spinner)
            print('Finished')
        else:
            print('No Data Processing Selected')
        return(self.data)

    
    @param.depends('process',watch=True)
    def view_grid(self):
        if self.process==True:
            self.param['view_processed'].constant=False
            self.param['fields'].constant        =False
        else:
            self.param['view_processed'].constant=True
            self.param['fields'].constant        =True
            
    @param.depends('fields',watch=True)
    def grid_selection(self):
        if self.fields == 'Grids':
            self.param['grids'].constant  = False
        else:
            self.param['grids'].constant  = True
            

#     def view(self):
#         return(test_plot(self.variable, self.time_step,self.time_window,self.density,self.weight,self.bins,self.get_date,self.maps))

#ADD NEW INSTANCE WHERE UPON SELECTED VIEW PROCESSED DATA - A NEW VIEW WILL BE CALLED AND SORTED AND GRIDDED DATA MAY BE VIEWED.

    @param.depends('time_window','time_step','density','weight','bins','get_date','maps','process','view_processed','fields','grids',watch=True)
    def view(self):
        if self.param['view_processed'].constant == True:
            data = fake_grid(None)
        else:
            data = self.data
        return(get_group(self.time_window,self.time_step,data,self.density,self.weight,self.bins,self.get_date,self.maps,self.process,self.view_processed,self.fields,self.grids))