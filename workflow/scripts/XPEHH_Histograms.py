#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 22:50:54 2022

@author: vishak
"""

import os
os.chdir("/home/vishak/GenomeIndia/XPEHH")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def Variant_Histogram():
    
    # Main Histogram
    fig = plt.figure(figsize = (22,7))
    #ax = fig.add_subplot(111)
    
    n, bins, patches = plt.hist(df['normxpehh'],100)
    plt.xticks(np.arange(min_value - 1.5, max_value + 1.5, 0.5))
    plt.xlabel('Normalized XP-EHH Scores')
    plt.xlim(min_value - 1.5 , max_value + 1.5)
    
    plt.ylabel('Number of Variants')
    plt.axvline(x = df_cutoff , color = 'black' , linestyle = '--')
    
    plt.title('Threshold: ' + str(round(df_cutoff , 4)))
    
    # Colormap
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    cm = plt.cm.get_cmap('viridis_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Inset Histogram
    a = plt.axes([0.17 , 0.4 , 0.2 , 0.4])
    interesting_df = df[df['normxpehh'] >= df_cutoff]
    n , bins , patches = plt.hist(interesting_df['normxpehh'], 100)
    plt.xticks(list(np.arange(math.floor(df_cutoff) , max_value + 1.5 , 1)))
    plt.xlabel('Normalized XP-EHH Scores')
    plt.ylabel('Number of Variants')
    plt.title('Top 1% Variants')
    
    # Colormap
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    cm = plt.cm.get_cmap('viridis_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    plt.savefig('OWN_EUR iHS Variant Histogram.png' , format = 'png' , dpi = 600)



df = pd.read_table("OWN_EUR.Complete.xpehh.out.norm")
df_cutoff = np.percentile(df['normxpehh'] , 99)
max_value = round(max(df['normxpehh']))
max_variants = len(df)
min_value = round(min(df['normxpehh']))

Variant_Histogram()