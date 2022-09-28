#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 20:10:15 2022

@author: cbr
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.lines import Line2D
from matplotlib import gridspec
import matplotlib as mpl

import gzip 
import sys
import getopt

if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["input_pop=", "bins=", "threshold=", "region_size=", "region_cutoff=", "chromosome="]
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
            params['inputpop'] = arg
            
        elif opt in ["--bins"]:
            params['bins'] = arg
            
        elif opt in ["--threshold"]:
            params['threshold'] = arg
            
        elif opt in ["--region_size"]:
            params['region_size'] = arg
            
        elif opt in ["--region_cutoff"]:
            params['region_cutoff'] = arg
            
        elif opt in ["--chromosome"]:
            params['chromosome'] = arg

#params = {}
#params['inputpop'] = '/home/cbr/iHS/7_Normalization/40_bins/Deshastha_Brhamin/Deshastha_Brhamin'
#params['bins'] = 40
#params['threshold'] = 99
#params['region_size'] = 200000
#params['region_cutoff'] = 20
#params['chromosome'] = 22

# Data Manipulation
df = pd.read_table(params['inputpop']+ '_iHS_Complete.norm')
#df = pd.read_table("iHS_Complete.norm")
df['index'] = list(df.index)
df_cutoff = np.percentile(df['ABS_normihs'] , int(params['threshold']))
df['colors'] = np.where(df['Chr']%2 == 1, 'gray' , 'cornflowerblue')

interesting_vars = df[df['ABS_normihs'] >= df_cutoff]
interesting_vars['colors'] = np.where(interesting_vars['Chr']%2 == 1 , 'orange' , 'coral')
interesting_vars_pos = list(interesting_vars.index)
df.drop(interesting_vars_pos, inplace = True)
df = pd.concat([df , interesting_vars])


# Extra Information
chr_len = {1 : '248956422', 2 : '242193529', 3 : '198295559', 4 : '190214555',
           5 : '181538259', 6 : '170805979', 7 : '159345973', 8 : '145138636',
           9 : '138394717', 10 : '133797422', 11 : '135086622', 12 : '133275309',
           13 : '114364328', 14 : '107043718', 15 : '101991189', 16 : '90338345',
           17 : '83257441', 18 : '80373285', 19 : '58617616', 20 : '64444167',
           21 : '46709983',22 : '50818468'}


# Finding Regions
complete_df = pd.DataFrame(columns = ['SNP ID' , 'pos' , 'ihs' , 'normihs' , 'Chr',
                                      'ABS_normihs' , 'index', 'colors' , 'fraction'])
regions = []
for i in range(1,int(params['chromosome']) + 1):
    chr_df = df[df['Chr'] == i]
    
    for j in range(0, int(chr_len[i]) , int(params['region_size'])):
        focus_df = chr_df[chr_df['pos'] >= j]
        focus_df = focus_df[focus_df['pos'] <= j + int(params['region_size']) - 1]
      
        if len(focus_df) == 0:
            continue
        
        elif len(focus_df[focus_df['ABS_normihs'] >= df_cutoff]) < int(params['region_cutoff']):
            continue
        
        else:
            no_good_vars = len(focus_df[focus_df['ABS_normihs'] >= df_cutoff])
            no_bad_vars = len(focus_df[focus_df['ABS_normihs'] < df_cutoff])
            total_vars = len(focus_df)
            fraction_good_vars = no_good_vars/total_vars
            regions.append([i , j , fraction_good_vars])
            focus_df['fraction'] = fraction_good_vars
            
            complete_df = pd.concat([complete_df , focus_df])

regions_df = pd.DataFrame(regions , columns = ['Chromosome' , 'Region' , 'Fraction'])
regions_df['Fraction_Percentage'] = regions_df['Fraction']*100
regions_df['Rounded_Fraction'] = round(regions_df['Fraction_Percentage'])


# Plotting
# ColorMaps
cmap = mpl.cm.get_cmap('Greens')
cbar = mpl.colors.ListedColormap([cmap(0.1), cmap(0.2), cmap(0.3), cmap(0.4), cmap(0.5),
                                  cmap(0.6), cmap(0.7), cmap(0.8), cmap(0.9), cmap(1.0)])
colors = cbar.colors
window_colors = {}
for i in range(len(colors)):
    window_colors[(i+1)*10] = colors[i]

# Creating Figure
fig = plt.figure(figsize = (22,7))
gs = gridspec.GridSpec(2 , 1 , height_ratios=[20, 1])


ax2 = fig.add_subplot(gs[1])
ax = fig.add_subplot(gs[0])

# Figure 1 - Manhattan Plot
df_grouped = df.groupby(('Chr'))
x_labels = []
x_labels_pos = []
for num, (name, group) in enumerate(df_grouped):
    group.plot(kind = 'scatter' , x = 'index' , y = 'ABS_normihs' , color = group['colors'], ax = ax, s = 1)
    x_labels.append(int(name))
    x_labels_pos.append((group['index'].iloc[-1] - (group['index'].iloc[-1] - group['index'].iloc[0])/2))


# Figure 2 - Region Plot
regions_df['Bottom_Percent'] = [math.ceil(regions_df['Rounded_Fraction'][i]/10)*10 for i in range(len(regions_df))]
regions_df['Color'] = [window_colors[regions_df['Bottom_Percent'][i]] for i in range(len(regions_df))]

for i in range(1,int(params['chromosome']) + 1):
    chr_region = regions_df[regions_df['Chromosome'] == int(i)]
    
    if len(chr_region) == 0:
        continue
    else:
        max_region = max(chr_region['Region'])
        min_region = min(chr_region['Region'])
        chr_region['Normalized Region'] = (chr_region['Region'] - min_region)/(max_region - min_region) + (i-1)
        chr_region.reset_index(inplace = True, drop = True)
        
        for j in range(len(chr_region)):
            ax2.axvspan(xmin = chr_region['Normalized Region'][j],
                        xmax = chr_region['Normalized Region'][j],
                        ymin = 0.2,
                        ymax = 1,
                        color = chr_region['Color'][j])
            

# Beautifying Plot 1
ax.set_ylabel('|Normalized iHS|')
ax.spines['bottom'].set_visible(False)
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
ax.axhline(y = df_cutoff, color = 'black' , linestyle = '--')
ax.set_xticks([])
#ax.set_xticklabels(x_labels)
ax.set_xlabel('')
ax.set_title('Normalized iHS Score')

# Beautifying Plot 2

#ax2.spines['bottom'].set_visible(False)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
#ax2.spines['right'].set_visible(False)
#ax2.spines['left'].set_visible(False)
ax2.set_xlabel('Chromosome')

plt.subplots_adjust(hspace = 0, wspace = 0)

# Creating Colorbar
points = round(10/9,3)/10
half_points = round(points/2,3)
ticks = [i+half_points for i in np.arange(0 , 1.0 , points)]
clrbar = fig.colorbar(plt.cm.ScalarMappable(cmap = cbar),ax = [ax,ax2],
             orientation = 'vertical',
             #shrink = 0.2,
             aspect = 15,
             ticks = [0.05 , 0.15 , 0.25 , 0.35 , 0.45 , 0.55 , 0.65 , 0.75 , 0.85 , 0.95],
             #ticks = ticks,
             label = '|iHS| Variants Percentage in Regions',
             pad = 0.01,
             fraction = 0.10)

clrbar.ax.set_yticklabels(['0-10' , '10-20' , '20-30' , '30-40' , '40-50' , '50-60',
                           '60-70' , '70-80' , '80-90' , '90-100'])

plt.savefig(params['inputpop'] + "_iHS_Manhattan_Plot.png" , format = 'png' , dpi = 400)

complete_df.to_csv(params['inputpop'] + '_iHS_Interesting_Variants.tsv' , sep = '\t', index = None)

regions_df.to_csv(params['inputpop'] + '_iHS_Interesting_Regions.tsv' , sep = '\t' , index = None)
