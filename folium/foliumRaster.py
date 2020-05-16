    # -*- coding: utf-8 -*-
#!/usr/bin/python

'''


Created Date: Tuesday, April 21th 2020, 10:27:15 am
Author: Gabriel Agustín Garcia
Copyright (c) 2020 Your Company
'''

import folium
import folium.plugins
from folium.plugins import MousePosition
from folium.plugins import HeatMap


import glob
import os

import numpy as np
import numpy.ma as ma
import pandas as pd

import functions

import matplotlib.pyplot as plt
from matplotlib import cm

import branca

from folium.plugins import MousePosition

import rasterio
import rasterio.plot as plot
from rasterio import warp
from rasterio import windows

from matplotlib.patches import Rectangle



def  plot_raster(path_in,name_in, path_out,name_out, name_product):
    """ 
    Parameters:
    -----------
    pathIn : path of the folder where is netCDF files
    pathOut : path of the folder where .png files will be created
    Returns: 
    --------
    """  

    
    src = rasterio.open(path_in + name_in)
    # img = src.read()
    
    slice_ = (slice(0,src.height),slice(0,src.width))
    window_slice = windows.Window.from_slices(*slice_)
    print(window_slice)


    # datos_b1 = src.read(1)
    # plt.imshow(datos_b1)
    # ax = plt.gca()
    # ax.add_patch(Rectangle((window_slice.col_off,window_slice.row_off),
    #                     width=window_slice.width,
    #                     height=window_slice.height,fill=True,alpha=.2,
    #                 color="red"))
    # plt.show()
    bbox = windows.bounds(window_slice,src.transform)
    
    transform_window = windows.transform(window_slice,src.transform)

    # Read img and convert to rgb
    img = np.stack([src.read(4-i, window=window_slice) for i in range(1,4)],
                axis=-1)
    img = np.clip(img,0,2200)/2200

    print(img.shape)
    # plt.figure(figsize=(8,8))
    # plot.show(img.transpose(2,0,1),
    #         transform=transform_window, )
    
    transform,width,height = warp.calculate_default_transform(src.crs, {"init":"epsg:4326"},
                                                            img.shape[1],img.shape[0],
                                                            left=bbox[0],bottom=bbox[1],
                                                            right=bbox[2],top=bbox[3],
                                                            resolution=0.0002)

    out_array = np.ndarray((img.shape[2],height,width),dtype=img.dtype)

    warp.reproject(np.transpose(img,axes=(2,0,1)),
                out_array,src_crs=src.crs,dst_crs={"init":"epsg:4326"},
                src_transform=transform_window,
                dst_transform=transform,resampling=warp.Resampling.bilinear)

    bounds_trans = warp.transform_bounds(src.crs,{'init': 'epsg:4326'},*bbox)
    
    # plt.figure(figsize=(10,8))
    # plot.show(out_array,
    #         transform=transform, cmap='viridis')



    
    # print(src.crs)
    # print(type(img))
    # print(img.shape)

    # xx= src.bounds
    # bounds = [[xx[0], xx[1]], [xx[2], xx[3]]]
    # bounds = [[ymin, xmin], [ymax, xmax]]
    
    # out_array = np.ndarray((img.shape[2],height,width),dtype=img.dtype)

    # warp.reproject(img,
    #             img,src_crs=src.crs,dst_crs={"init":"epsg:4326"})

    # plt.figure(figsize=(10,8))
    # plot.show(img)


    # # Setup colormap
    # colors = ['#d7191c',  '#fdae61',  '#ffffbf',  '#abdda4',  '#2b83ba']
    # vmin = np.nanmin(img)
    # vmax = np.nanmax(img)
    # print("Min: " + str(vmin))
    # print("Max: " + str(vmax))

    # levels = 15
    # cm = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(levels)
    # # Add the colormap to the folium map
    # cm.caption = "XCH4"

    # # define the world map centered around Canada with a low zoom level
    
    
    mean_lat = (bbox[1] + bbox[3]) / 2.0
    mean_lng = (bbox[0] + bbox[2]) / 2.0
    
    # world_map = folium.Map(location=[mean_lat,mean_lng], zoom_start=4)

    
    # # imageOverlay = folium.raster_layers.ImageOverlay(band, bounds, colormap=cm.viridis, opacity=0.5)
    # # world_map.add_child(imageOverlay)
    # # folium.TileLayer('openstreetmap').add_to(world_map)
    
    
    # image_overlay = folium.raster_layers.ImageOverlay(np.transpose(out_array,(1,2,0)),
    #                                     [[bounds_trans[1],
    #                                     bounds_trans[0]],
    #                                     [bounds_trans[3],
    #                                     bounds_trans[2]]],
    #                                     name="Satellogic")
    # world_map.add_child(image_overlay)
    
    
    map_bb = folium.Map(location=[mean_lat,mean_lng],
            zoom_start=8)
    
    folium.TileLayer('cartodbpositron').add_to(map_bb)
    
    folium.raster_layers.TileLayer(
        tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='google',
        name='google maps',
        max_zoom=20,
        subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
        overlay=False,
        control=True,
    ).add_to(map_bb)
    
    
    folium.raster_layers.TileLayer(
        tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr='google',
        name='google street view',
        max_zoom=20,
        subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
        overlay=False,
        control=True,
    ).add_to(map_bb)
    
    image_overlay = folium.raster_layers.ImageOverlay(np.transpose(out_array,(1,2,0)),
                                                    [[bounds_trans[1],
                                                        bounds_trans[0]],
                                                    [bounds_trans[3],
                                                        bounds_trans[2]]],
                                                    name=name_product)
    map_bb.add_child(image_overlay)
    folium.map.LayerControl(position='topright').add_to(map_bb)
    
    
    MousePosition().add_to(map_bb)

    map_bb.save(path_out + name_out)


if __name__ == "__main__":

    path_in = '/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/Plotly-Folium-test/folium/data/'
    name_in = '2017_09_30_S2_RGB.tif'
    
    path_out = '/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/Plotly-Folium-test/folium/images/'
    name_out = 'folium_plot_raster.html'
    
    name_product = 'Sentinel-2'
    
    plot_raster(path_in,name_in, path_out,name_out, name_product)









# # create a Stamen Toner map of the world centered around Canada
# world_map = folium.Map(location=[-31.627062, -60.702951], zoom_start=4, tiles='Stamen Terrain')
 
# # display world map

# world_map.save(f'/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/folium-test/images/folium_terrain.html')


