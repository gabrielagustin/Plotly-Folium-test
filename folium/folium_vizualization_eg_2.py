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


m = folium.plugins.DualMap(location=[lat, lon], tiles=None, zoom_start=8)

folium.TileLayer('openstreetmap').add_to(m.m1)
folium.TileLayer('openstreetmap').add_to(m.m2)
folium.TileLayer('cartodbpositron').add_to(m.m1)
folium.TileLayer('cartodbpositron').add_to(m.m2)

folium.LayerControl(collapsed=False).add_to(m)


MousePosition().add_to(m.m1)
MousePosition().add_to(m.m2)


m.save(f'/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/Plotly-Folium-test/folium/images/Folium_Vizualization_Eg_2.html')




