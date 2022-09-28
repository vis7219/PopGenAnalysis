#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 22:50:54 2022

@author: vishak
"""

import gzip 
import sys
import getopt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["input_pop=", "threshold="]
    try:
        opts, args = getopt.getopt(argv, smallflags, bigflags)
        if not opts:
            print("enter something")
            sys.exit(2)
    except getopt.GetoptError:
        print("Incorrect options passed")
        sys.exit(2)
        
        
    params = {}

    for opt, arg in opts:

        if opt in ["-K"]:
            params['K'] = int(arg)

        elif opt in ["--input_pop"]:
            params['input_pop'] = arg

        elif opt in ["--threshold"]:
            params['threshold'] = arg

def Region_Histogram():
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    n, bins, patches = ax.hist(df['Fraction_Percentage'],100)
    ax.set_xticks(np.arange(0, 110, 10))
    ax.set_xlabel('Percentage of variants with |iHS| value above threshold in a region')
    
    ax.set_ylabel('Number of Regions')
    plt.axvline(x = df_cutoff , color = 'black' , linestyle = '--')
    
    ax.set_title('Threshold: ' + str(round(df_cutoff , 4)))
    
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    cm = plt.cm.get_cmap('viridis_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
        
    # Inset Histogram
    a = plt.axes([0.65 , 0.4 , 0.2 , 0.4])
    interesting_df = df[df['Fraction_Percentage'] >= df_cutoff]
    n , bins , patches = plt.hist(interesting_df['Fraction_Percentage'], 100)
    plt.xticks(list(np.arange(math.floor((77/10))*10 , 110 , 10)))
    plt.xlabel('Percentage of variants with |iHS|value above threshold in a region')
    plt.ylabel('Number of Regions')
    plt.title('Top 1% Regions')
    
    # Colormap
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    cm = plt.cm.get_cmap('viridis_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
        
    plt.savefig(params['input_pop'] + '_iHS_Region_Histogram.png' , format = 'png' , dpi = 400)

def Variant_Histogram():
    
    # Main Histogram
    fig = plt.figure(figsize = (22,7))
    #ax = fig.add_subplot(111)
    
    n, bins, patches = plt.hist(df['ABS_normihs'],100)
    plt.xticks(np.arange(0, max_value + 1.5, 0.5))
    plt.xlabel('Normalized |iHS| Scores')
    
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
    a = plt.axes([0.65 , 0.4 , 0.2 , 0.4])
    interesting_df = df[df['ABS_normihs'] >= df_cutoff]
    n , bins , patches = plt.hist(interesting_df['ABS_normihs'], 100)
    plt.xticks(list(np.arange(math.floor(df_cutoff) , max_value + 1.5 , 1)))
    plt.xlabel('Normalized |iHS| Scores')
    plt.ylabel('Number of Variants')
    plt.title('Top 1% Variants')
    
    # Colormap
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    cm = plt.cm.get_cmap('viridis_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    plt.savefig(params['input_pop'] + '_iHS_Variant_Histogram.png' , format = 'png' , dpi = 400)


df = pd.read_table(params['input_pop'] + "_iHS_Interesting_Regions.tsv")
df_cutoff = np.percentile(df['Fraction_Percentage'] , params['threshold'])
max_value = round(max(df['Fraction_Percentage']))
max_variants = len(df)

Region_Histogram()

df = pd.read_table(params['input_pop'] + "_iHS_Complete.norm")
df_cutoff = np.percentile(df['ABS_normihs'] , params['threshold'])
max_value = round(max(df['ABS_normihs']))
max_variants = len(df)

Variant_Histogram()