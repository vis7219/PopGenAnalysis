#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 11:33:47 2022

@author: cbr
"""

import os
os.chdir("/home/vishak/GenomeIndia/XPEHH/")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data Manipulation
df = pd.read_table("OWN_AFR.Complete.xpehh.out.norm")
df.rename({'Unnamed: 0' : 'SNP ID'},
          inplace = True,
          axis = 1)

df_cutoff = np.percentile(list(df['normxpehh']), 99)
df['colors'] = np.where(df['Chr']%2 == 1, 'gray' , 'cornflowerblue')

interest_vars = df[df['normxpehh'] >= df_cutoff]
interest_vars['colors'] = np.where(interest_vars['Chr']%2 == 1 , 'orange' , 'saddlebrown')
vars_pos = list(interest_vars.index)
df.drop(vars_pos, inplace = True)
df = pd.concat([df , interest_vars])

df['index'] = list(df.index)

    
def XPEHH():
    #Plotting XP-EHH Manhattan Plot
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    df_grouped = df.groupby(('Chr'))
    
    x_labels = []
    x_labels_pos = []
    colors = ['gray']
    for num, (name, group) in enumerate(df_grouped):
        group.plot(kind = 'scatter' , x = 'index' , y = 'normxpehh' , color = group['colors'], ax = ax, s = 1)
        x_labels.append(int(name))
        x_labels_pos.append((group['index'].iloc[-1] - (group['index'].iloc[-1] - group['index'].iloc[0])/2))
    
    ax.set_xticks(x_labels_pos)
    ax.set_xticklabels(x_labels)
    ax.set_xlim([0, len(df)])
    ax.set_xlabel('Chromosome')
    
    plt.savefig("OWN_AFR_ManhattenPlot.png" , format = 'png')

def Histogram():
    # Plotting Histogram
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    n, bins, patches = ax.hist(df['normxpehh'],100)
    ax.set_xticks(np.arange(-6,6.5,0.5))
    ax.set_xlim(-6 , 6.5 , 0.5)
    
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    cm = plt.cm.get_cmap('hot_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
        
    plt.savefig("OWN_AFR_Complete_Histogram.png", format = 'png')

def XPEHH_200KB_Top1():      
    chr_len = {1 : '248956422', 2 : '242193529', 3 : '198295559', 4 : '190214555',
               5 : '181538259', 6 : '170805979', 7 : '159345973', 8 : '145138636',
               9 : '138394717', 10 : '133797422', 11 : '135086622', 12 : '133275309',
               13 : '114364328', 14 : '107043718', 15 : '101991189', 16 : '90338345',
               17 : '83257441', 18 : '80373285', 19 : '58617616', 20 : '64444167',
               21 : '46709983',22 : '50818468'}
    
    complete_focus_df = pd.DataFrame(columns = ['SNP ID' , 'pos' , 'xpehh' , 'normxpehh',
                                                'Chr' , 'colors' , 'index'])
    region_list = []
    
    for i in range(1,23):
        chr_df = df[df['Chr'] == i]
    
    
        for j in range(0, int(chr_len[i]) , 200000):
            focus_df = chr_df[chr_df['pos'] >= j]
            focus_df = focus_df[focus_df['pos'] <= j + 199999]
            
            if len(focus_df) == 0:
                continue
            else:
                focus_df_cutoff = max(list(focus_df['normxpehh']))
                focus_df = focus_df[focus_df['normxpehh'] == focus_df_cutoff]
                focus_df.reset_index(inplace = True , drop = True)
                
                complete_focus_df = pd.concat([complete_focus_df , focus_df])
                complete_focus_df.reset_index(inplace = True , drop = True)
                
                region_list.append([i , j , focus_df['SNP ID'][0] , focus_df['pos'][0],
                                   focus_df['normxpehh'][0]])
                
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    df_grouped = complete_focus_df.groupby(('Chr'))
    
    x_labels = []
    x_labels_pos = []
    for num, (name, group) in enumerate(df_grouped):
        group.plot(kind = 'scatter' , x = 'index' , y = 'normxpehh' , color = group['colors'], ax = ax, s = 1)
        x_labels.append(int(name))
        x_labels_pos.append((group['index'].iloc[-1] - (group['index'].iloc[-1] - group['index'].iloc[0])/2))
    
    ax.set_xticks(x_labels_pos)
    ax.set_xticklabels(x_labels)
    ax.set_xlim([0, len(df)])
    ax.set_xlabel('Chromosome')
    
    plt.savefig("OWN_AFR.ManhattenPlot.png" , format = 'png' , dpi = 400)
    return(complete_focus_df , region_list)
    
#chrom_XPEHH()
#XPEHH()
#Histogram()
#XPEHH_200KB_Top1percent()
complete_df , region_list = XPEHH_200KB_Top1()

#region_df = pd.DataFrame(region_list , columns = ['Chromosome' , 'Region' , 'SNP ID',
#                                                  'pos' , 'normxpehh'])

#complete_df.to_csv("AFR Interesting Variants.tsv" , index = None , sep = '\t')
#region_df.to_csv('AFR Interesting Regions.tsv' , index = None , sep = '\t')