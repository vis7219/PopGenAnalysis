#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 14:33:30 2022

@author: cbr
"""

import os
os.chdir("/home/vishak/iHS/7_Normalization/40_bins")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.lines import Line2D
from matplotlib import gridspec
import matplotlib as mpl

df = pd.read_excel('Top10.xlsx')
df.set_index('Region' , inplace = True)



f = plt.figure(dpi = 300 , figsize = (10,20))
#f.set_figwidth(10)
plt.imshow(df , cmap = 'hot_r')
plt.xticks([0 , 1 , 2 , 3 , 4,
            5 , 6 , 7 , 8 , 9,
            10 , 11 , 12], ['Adikarnataka' , 'Deshastha Brahmin',
                                 'Iyengar' , 'Kolis' , 'Konkanastha Brahmin',
                                 'Lingayath' , 'Marathas' , 'Nadar' , 'Naidu',
                                 'Namboodari' , 'Parayan' , 'Vakkaliga',
                                 'Vidiki Brahmin'], rotation = 90)
plt.xlabel('Ethnicities')
plt.yticks(list(range(0,61)) , list(df.index) , rotation = 50)
plt.ylabel('Regions')
cbar = plt.colorbar(label = '|iHS| Variants Percentage' , orientation = 'vertical')
cbar.ax.tick_params(rotation=90)

f.savefig("iHS Heatmap.png" , format = 'png')





#x = list(range(0,43))


