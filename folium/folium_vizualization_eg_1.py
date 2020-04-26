# -*- coding: utf-8 -*-
#!/usr/bin/python

'''


Created Date: Tuesday, April 25th 2020, 19:17:15 am
Author: Gabriel Agustín Garcia
Copyright (c) 2020 Your Company
'''

import folium
from folium.plugins import MousePosition


lon, lat = -60.702951, -31.627062


m = folium.Map(location=[lat, lon], zoom_start=8, tiles=None)

folium.TileLayer('openstreetmap').add_to(m)

folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='google',
    name='google maps',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(m)

folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr='google',
    name='google street view',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(m)

# folium.raster_layers.WmsTileLayer(
#     url='http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi',
#     name='test',
#     fmt='image/png',
#     layers='nexrad-n0r-900913',
#     attr=u'Weather data © 2012 IEM Nexrad',
#     transparent=True,
#     overlay=True,
#     control=True,
# ).add_to(m)

### add mouse position
folium.LayerControl().add_to(m)



MousePosition().add_to(m)


m.save(f'/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/Plotly-Folium-test/folium/images/Folium_Vizualization_Eg_1.html')


