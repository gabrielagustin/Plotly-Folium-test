import pandas as pd


import glob

import geopandas as gpd
# import matplotlib.pyplot as plt
import numpy as np
# from matplotlib import cm
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# from shapely.geometry import Point, Polygon

import plotly.express as px

import functions

# pathIn = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/Max/"
# pathOut = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/PNG/Max/"


pathIn = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/Min/"
pathOut = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/PNG/Min/"

# pathIn = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/Mean/"
# pathOut = "/media/ggarcia/data/Satellogic/Satellogic/Data/Neuquen/Sentinel-5p-L3_CH4(Methane)/PNG/Mean/"


# se listan todos los archivos .tif que pertenecen a las imagenes SAR Sentinel 1
files = sorted([f for f in glob.glob(pathIn + "**/*.tif", recursive=True)])


# path al geojson del pais

argentina_fp = "/media/ggarcia/data/Satellogic/Satellogic/Data/SIG_Argentina/provincia.json"
provincias = gpd.read_file(argentina_fp)

print(type(provincias))


###  La Pampa, Neuquén, Río Negro, Chubut, Santa Cruz y Tierra del Fuego, Antártida e Islas del Atlántico Sur
patagonia = [ 'Neuquén'] ### 'Mendoza', 'Chubut', 'Santa Cruz', 'La Pampa', 'Río Negro'

map_dep1 = provincias[provincias.nam.isin(patagonia)]

gridCRS = map_dep1.crs
print(gridCRS)

for i in range(0, 1):
    
    # fig, ax = plt.subplots(1)
    print(files[i])
    name = files[i]
    ### for min and max
    date = name[87:-8]
    ### for mean
    # date = name[88:-9]
    print("date: "+str(date))

    src_ds, band, GeoT, Project = functions.openFileHDF(files[i], 1)

    # print(Project)
    xmin,xmax,ymin,ymax=GeoT[0],GeoT[0]+GeoT[1]*src_ds.RasterXSize,GeoT[3]+GeoT[5]*src_ds.RasterYSize,GeoT[3]

    # cmap = cm.colors.ListedColormap(['royalblue', 'cyan',
    #                                   'yellow', 'orange'])
    # cmap.set_over('red')
    # cmap.set_under('blue')

    # maxV = []
    # maxV.append(np.nanmax(band))
    # minV = []
    # minV.append(np.nanmin(band))


    # fig, ax = plt.subplots(figsize = (15,15))
    # plt.title('XCH4    '+'Date: ' + str(date))
    # ## Units: ppmv (parts per million by volume)
    # im = ax.imshow(band, extent=[xmin,xmax,ymin,ymax], vmin=1700, vmax=1850, cmap=plt.get_cmap('jet'), interpolation='nearest', aspect='auto')
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)
    # fig.colorbar(im, cax=cax, label='[ppmv]')

    ## capital de Neuquen

    # lat_point = [-38.98583333]
    # lon_point = [-68.06416667]
    # point_geom = Point(zip(lon_point, lat_point))
    # crs = {'init': 'epsg:4326'}
    # point = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[point_geom])
    # point.plot(ax=ax, marker='o', color='blue', markersize=20)


    # map_dep1.plot(ax=ax, alpha=0.2, edgecolor='k')
    
    
    fig = px.imshow(band)
    # fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                            # color_discrete_sequence=["fuchsia"], zoom=3, height=900)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()



    
    
    # plt.show()
