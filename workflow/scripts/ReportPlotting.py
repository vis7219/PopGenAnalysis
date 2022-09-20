#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 17:26:51 2022

@author: cbr
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import getopt


if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["afreq=", "hardy=", "het=", "smiss=", "vmiss=", "id=", "outpath=", "qcstep="]
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

        elif opt in ["--afreq"]:
            params['afreq'] = arg

        elif opt in ["--hardy"]:
            params['hardy'] = arg
        
        elif opt in ["--het"]:
            params['het'] = arg
            
        elif opt in ["--smiss"]:
            params['smiss'] = arg
            
        elif opt in ["--vmiss"]:
            params['vmiss'] = arg
            
        elif opt in ["--id"]:
            params['id'] = arg
            
        elif opt in ["--outpath"]:
            params['outpath'] = arg
        
        elif opt in ['--qcstep']:
            params['qcstep'] = arg


def AlleleFrequencyPlot(afreq_file, sample_id , outpath, qcstep):
    # Import Data
    afreq = pd.read_table(afreq_file)
    afreq = list(afreq['ALT_FREQS'])
    
    
    # Create figure & axes
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    # Plot Histogram
    n, bins, patches = ax.hist(afreq, 10)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    
    # Custom coloring histogram
    cm = plt.cm.get_cmap('RdYlBu_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Adding values to bars
    ax.bar_label(patches)
    
    
    # Visual Changes
    ax.set_title(str(sample_id) + ": " + str(qcstep) + "-afreq Plot")
    #ax.set_title("1011GI: Changed Missing IDs Allele Frequency")
    ax.set_xlabel("Allele Frequency" , fontsize = 12)
    ax.set_ylabel("No. of Variants" , fontsize = 12)
    ax.set_xticks(np.arange(0.0 , 1.1 , 0.1))
    
    fig.savefig(str(outpath) + '/' + str(sample_id) + ':' + str(qcstep) + "_AlleleFrequency.jpeg",
                format = 'jpeg',
                dpi = 300)
    #fig.savefig("1011GI:ChangedMissingIDs_AlleleFrequency.jpeg", format = 'jpeg' , dpi = 600)
    
def HardyPlot(hardy_file, sample_id , outpath , qcstep):
    # Import Data
    hardy = pd.read_table(hardy_file)
    hardy = list(hardy['P'])
    
    # Create figure & axes
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    # Plot Histogram
    n, bins, patches = ax.hist(hardy, 10)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    
    # Custom coloring histogram
    cm = plt.cm.get_cmap('RdYlBu_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Adding values to bars
    ax.bar_label(patches)
    
    # Visual Changes
    ax.set_title(str(sample_id) + ": " + str(qcstep) + "-Hardy Plot")
#    ax.set_title("1011GI: Changed Missing IDs Hardy-Weinberg Equilibrium")
    ax.set_xlabel("P value" , fontsize = 12)
    ax.set_ylabel("No. of Variants" , fontsize = 12)
    ax.set_xticks(np.arange(0.0 , 1.1 , 0.1))
    
    #fig.savefig("1011GI:ChangedMissingIDs_HWE.jpeg", format = 'jpeg' , dpi = 600)
    fig.savefig(str(outpath) + '/' + str(sample_id) + ':' + str(qcstep) + "_HWE.jpeg",
                format = 'jpeg',
                dpi = 300)

def HeterozygosityPlot(het_file , sample_id , outpath , qcstep):
    # Import Data
    het = pd.read_table(het_file)
    het['het_rate'] = (het['OBS_CT'] - het['O(HOM)'])/het['OBS_CT']
    het = list(het['het_rate'])
    
    # Create figure & axes
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    # Plot Histogram
    n, bins, patches = ax.hist(het)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    bins = list(bins)
    bins_name = [round(i,2) for i in bins]
    
    # Custom coloring histogram
    cm = plt.cm.get_cmap('RdYlBu_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Adding values to bars
    #ax.bar_label(patches)
    for containers in ax.containers:
        ax.bar_label(containers)
    
    # Visual Changes
    ax.set_title(str(sample_id) + ": " + str(qcstep) + "-Het Plot")
    #ax.set_title("1011GI: Changed Missing IDs Heterozygosity")
    ax.set_xlabel("Het rate" , fontsize = 12)
    ax.set_ylabel("No. of Individuals" , fontsize = 12)
    ax.set_xticks(bins, bins_name)
    
    #fig.savefig("1011GI:ChangedMissingIDs_Het.jpeg", format = 'jpeg' , dpi = 600)
    fig.savefig(str(outpath) + '/' + str(sample_id) + ':' + str(qcstep) + "_Heterozygosity.jpeg",
                format = 'jpeg',
                dpi = 300)

def SamplemissingPlot(smiss_file , sample_id , outpath , qcstep):
    # Import Data
    smiss = pd.read_table(smiss_file)
    smiss = list(smiss['F_MISS'])
    
    # Create figure & axes
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    # Plot Histogram
    n, bins, patches = ax.hist(smiss)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    
    # Custom coloring histogram
    cm = plt.cm.get_cmap('RdYlBu_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Adding values to bars
    #ax.bar_label(patches)
    for containers in ax.containers:
        ax.bar_label(containers)
    
    # Visual Changes
    ax.set_title(str(sample_id) + ": " + str(qcstep) + "-smiss Plot")
    #ax.set_title("1011GI: Changed Missing IDs Sample Missingness")
    ax.set_xlabel("Missingness" , fontsize = 12)
    ax.set_ylabel("No. of Individuals" , fontsize = 12)
    ax.set_xticks(np.arange(0 , 1.1 , 0.1))
    
    #fig.savefig("1011GI:ChangedMissingIDs_SampleMissing.jpeg", format = 'jpeg' , dpi = 600)
    fig.savefig(str(outpath) + '/' + str(sample_id) + ':' + str(qcstep) + "_SampleMissingness.jpeg",
                format = 'jpeg',
                dpi = 300)

def VariantmissingnessPlot(vmiss_file , sample_id , outpath , qcstep):
    # Import Data
    vmiss = pd.read_table(vmiss_file)
    vmiss = list(vmiss['F_MISS'])
    
    # Create figure & axes
    fig = plt.figure(figsize = (22,7))
    ax = fig.add_subplot(111)
    
    # Plot Histogram
    n, bins, patches = ax.hist(vmiss)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    
    # Custom coloring histogram
    cm = plt.cm.get_cmap('RdYlBu_r')
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Adding values to bars
    #ax.bar_label(patches)
    for containers in ax.containers:
        ax.bar_label(containers)
    
    # Visual Changes
    ax.set_title(str(sample_id) + ": " + str(qcstep) + "-vmiss Plot")
    #ax.set_title("1011GI: Changed Missing IDs Variant Missingness")
    ax.set_xlabel("Missingness" , fontsize = 12)
    ax.set_ylabel("No. of Variants" , fontsize = 12)
    ax.set_xticks(np.arange(0 , 1.1 , 0.1))
    
    #fig.savefig("1011GI:ChangedMissingIDs_VariantMissing.jpeg", format = 'jpeg' , dpi = 600)
    fig.savefig(str(outpath) + '/' + str(sample_id) + ':' + str(qcstep) + "_VariantMissingness.jpeg",
                format = 'jpeg',
                dpi = 300)

AlleleFrequencyPlot(params['afreq'] , params['id'] , params['outpath'], params['qcstep'])
HardyPlot(params['hardy'] , params['id'] , params['outpath'] , params['qcstep'])
HeterozygosityPlot(params['het'] , params['id'] , params['outpath'], params['qcstep'])
SamplemissingPlot(params['smiss'] , params['id'] , params['outpath'], params['qcstep'])
VariantmissingnessPlot(params['vmiss'] , params['id'] , params['outpath'], params['qcstep'])