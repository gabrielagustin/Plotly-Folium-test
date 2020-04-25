# -*- coding: utf-8 -*-
#!/usr/bin/python

'''


Created Date: Tuesday, April 21th 2020, 10:27:15 am
Author: Gabriel Agustín Garcia
Copyright (c) 2020 Your Company
'''

import folium

# define the world map centered around Canada with a low zoom level
world_map = folium.Map(location=[-31.627062, -60.702951], zoom_start=4)

# display world map
world_map.save(f'/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/folium-test/images/folium_world_map.html')


# create a Stamen Toner map of the world centered around Canada
world_map = folium.Map(location=[-31.627062, -60.702951], zoom_start=4, tiles='Stamen Terrain')
 
# display world map

world_map.save(f'/media/ggarcia/data/Satellogic/Satellogic/Tests/GitHubTest/folium-test/images/folium_terrain.html')


