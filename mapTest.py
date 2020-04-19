#!/usr/bin/python

'''
Created on Tuesday, January 28th 2020, 2:31:18 pm
Author: Gabriel Garcia

Copyright (c) 2020 Your Company
'''

import glob
import pandas as pd
from netCDF4 import Dataset
import numpy as np

import plotly.express as px





def plot_NC_file(pathIn, pathOut):
    """ 
    Parameters:
    -----------
    pathIn : path of the folder where is netCDF files
    pathOut : path of the folder where .png files will be created
    Returns: 
    --------
    """

    # se listan todos los archivos .tif que pertenecen a las imagenes SAR Sentinel 1
    files = sorted([f for f in glob.glob(pathIn + "*.nc", recursive=True)])


    for i in range(0, 1):
        # print(files[i])

        nc_f = files[i]
        # nc_f = path + netcd_fname
        
        # print(nc_f)
        
        date = files[i][106:-58]
        print("date:" + str(date))

        ### Dataset is the class behavior to open the file
        ### and create an instance of the ncCDF4 class    
        nc_file = Dataset(nc_f, 'r')  

        ### para ver el el contenido del archivo .nc en diferentes niveles
        # print (nc_file.groups)
        # print (nc_file.groups['PRODUCT'].variables.keys())
        # print (nc_file.groups['PRODUCT'].variables[ 'methane_mixing_ratio'])

        lons = nc_file.groups['PRODUCT'].variables['longitude'][:][0,:,:]
        lats = nc_file.groups['PRODUCT'].variables['latitude'][:][0,:,:]
        
        XCH4 = nc_file.groups['PRODUCT'].variables['methane_mixing_ratio'][0,:,:]


        d = {'XCH4': np.array(XCH4).flatten(), 'lat': np.array(lats).flatten(), 'lon': np.array(lons).flatten()}

        df = pd.DataFrame(data=d)   
        
        df = df[(df['XCH4'] >= 1300) & (df['XCH4'] <=2100 )]

        fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="XCH4", hover_data=["XCH4"],
                                 color="XCH4", color_continuous_scale=px.colors.cyclical.IceFire, zoom=3, height=900)
        
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()








if __name__ == "__main__":
    ### Path of netCDF file
    pathIn = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/NC/"
    pathOut = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/NC/PNG/"
    plot_NC_file(pathIn, pathOut)


