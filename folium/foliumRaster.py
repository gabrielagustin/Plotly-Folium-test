# -*- coding: utf-8 -*-
#!/usr/bin/python

'''


Created Date: Tuesday, April 21th 2020, 10:27:15 am
Author: Gabriel Agustín Garcia
Copyright (c) 2020 Your Company
'''


import folium
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.plot as plot
from folium.plugins import MousePosition

from rasterio import warp


def  plot_raster(path_in,name_in, path_out,name_out, name_product):
    """ 
    Parameters:
    -----------
    path_in: path of the folder where is netCDF files
    name_in: name of .tif file
    path_out: path of the folder where .png files will be created
    name_out: name of HTML file to be created
    name_product: name of product to plot
    Returns: 
    --------
    None: create a HTML file
    """  

    ### read raster file
    src = rasterio.open(path_in + name_in)
    bbox = src.bounds
    
    # Read img and convert to rgb
    img = np.stack([src.read(4-i) for i in range(1,4)],
               axis=-1)
    transform,width,height = warp.calculate_default_transform(src.crs, {"init":"epsg:4326"},
                                                          img.shape[1],img.shape[0],
                                                          left=bbox[0],bottom=bbox[1],
                                                          right=bbox[2],top=bbox[3],
                                                          resolution=0.002)

    out_array = np.ndarray((img.shape[2],img.shape[0],img.shape[1]),dtype=img.dtype)

    warp.reproject(np.transpose(img,axes=(2,0,1)),
                out_array,src_crs=src.crs,dst_crs={"init":"epsg:4326"},
                src_transform=transform,
                dst_transform=transform,resampling=warp.Resampling.bilinear)
        
    bounds_trans = warp.transform_bounds(src.crs,{'init': 'epsg:4326'},*bbox)     
    
    # plt.figure(figsize=(10,8))
    # plot.show(out_array,
    #         transform=transform)

    ### define the world map centered around center of tif image
    
    mean_lat = (bbox[1] + bbox[3]) / 2.0
    mean_lng = (bbox[0] + bbox[2]) / 2.0
    
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
    
    ### add mouse positio
    MousePosition().add_to(map_bb)
    ### create a .html file
    map_bb.save(path_out + name_out)


if __name__ == "__main__":

    path_in = '/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/Plotly-Folium-test/folium/data/'
    name_in = '2017_09_30_S2_RGB.tif'
    
    path_out = '/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/Plotly-Folium-test/folium/images/'
    name_out = 'folium_plot_raster.html'
    
    name_product = 'Sentinel-2'
    
    plot_raster(path_in,name_in, path_out,name_out, name_product)