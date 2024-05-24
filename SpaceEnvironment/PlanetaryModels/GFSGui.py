# Download and display Global Forecast System data

import matplotlib.pyplot as plt
from siphon.catalog import TDSCatalog
from datetime import datetime
from xarray.backends import NetCDF4DataStore
import xarray as xr
import FreeSimpleGUI as sg

# This script creates a GUI to allow you choose to display various Global Forcast System (for Earth)
# maps/plots such as temperature, pressure, wind speed I believe and others. Give it a try and let 
# me know if it works!

best_gfs = TDSCatalog('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/'
                      'Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best')

best_ds = list(best_gfs.datasets.values())[0]
ncss = best_ds.subset()

query = ncss.query()

variables = str(ncss.variables).strip('{}').split(', ')
variables = [variable.strip("'") for variable in variables]

query.lonlat_box(north=90, south=-90, east=180, west=-180).time(datetime.utcnow())
query.accept('netcdf4')

sg.theme("DarkBlue")

layout = [
    [sg.Listbox(variables, size=(70, 20), key='-LISTBOX-')],
    [sg.Submit()]
]
window = sg.Window('GFS Selector', layout, finalize=True, grab_anywhere=True)
listbox = window['-LISTBOX-'].Widget
print(variables)
while True:
    event, value = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "Submit":

        propertyrequest = value['-LISTBOX-'][0]
        query.variables(propertyrequest)

        data = ncss.get_data(query)
        data = xr.open_dataset(NetCDF4DataStore(data))

        variable_to_plot = data[propertyrequest]

        variable_to_plot.plot()

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(propertyrequest)

        plt.show()

window.close()
