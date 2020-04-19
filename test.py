# -*- coding: utf-8 -*-
#!/usr/bin/python

'''

Created on Tue Feb  5 10:58:49 2020
Author: Gabriel Agustín Garcia
Copyright (c) 2020 Your Company
'''

import os
import plotly.graph_objects as go
import numpy as np
np.random.seed(1)


# print(os.path.dirname(__file__).exists("images"))

# if not os.path.exists("images"):
#     os.mkdir("images")

filepath =  os.path.dirname(__file__)
print(filepath)

N = 100
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
sz = np.random.rand(N) * 30

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="markers",
    marker=go.scatter.Marker(
        size=sz,
        color=colors,
        opacity=0.6,
        colorscale="Viridis"
    )
))

# fig.write_image(filepath + "/images/fig1.png")

fig.write_html(filepath + "/test.html")

fig.show()

# fig.write_image(filepath +"/fig1.webp")