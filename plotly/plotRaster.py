#!/usr/bin/python

'''
Created on Tuesday, January 28th 2020, 2:31:18 pm
Author: Gabriel Garcia

Copyright (c) 2020 Your Company
'''


import glob
import os

import numpy as np
import pandas as pd
import plotly.express as px

import functions
import plotly.graph_objects as go


def plot_raster(fileIn, pathOut):
    """ Function that read raster file and graph it 
    using plotly library
    Parameters:
    -----------
    pathIn : path of the folder where is netCDF files
    pathOut : path of the folder where .png files will be created
    Returns: 
    --------
    """
    ### obtain image date from the nameFile
    name = fileIn
    date = name[88:-9]
    print("date: "+str(date))

    ### Read raster
    src_ds, band, GeoT, Project = functions.openFileHDF(files[i], 1)
    xmin,xmax,ymin,ymax=GeoT[0],GeoT[0]+GeoT[1]*src_ds.RasterXSize,GeoT[3]+GeoT[5]*src_ds.RasterYSize,GeoT[3]
   

    fig = px.imshow(band)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
    title={
        'text': "XCH4 -"+str(date),
        'y':0.05,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    
    fig.show()
    

if __name__ == "__main__":
    ### Path of netCDF file
    pathIn = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/Mean/"
    pathOut = "/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/Plotly-Folium-test/plotly/images/"
    # se listan todos los archivos .tif que pertenecen a las imagenes SAR Sentinel 1
    files = sorted([f for f in glob.glob(pathIn + "*.tif", recursive=True)])

    # for i in range(0, len(files),3):
    for i in range(0, 1):
    
        print(files[i])
        fileIn = files[i]
        plot_raster(fileIn, pathOut)
