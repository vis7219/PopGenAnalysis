#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 11:09:08 2022

@author: cbr
"""


import gzip 
import sys
import getopt
import pandas as pd

if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["file=", "own=", "ref="]
    try:
        opts, args = getopt.getopt(argv, smallflags, bigflags)
        if not opts:
            print("Enter Something")
            sys.exit(2)
    except getopt.GetoptError:
        print("Incorrect options passed")
        sys.exit(2)
        
        
    params = {}

    for opt, arg in opts:

        if opt in ["-K"]:
            params['K'] = int(arg)

        elif opt in ["--file"]:
            params['file'] = arg

        elif opt in ["--own"]:
            params['own_filename'] = arg
            
        elif opt in ["--ref"]:
            params['ref_filename'] = arg


file = pd.read_csv(params['file'])

try:
    ref_remove = pd.read_table("results/1_QualityCheck/8_Heterozygosity/8.4_" +
                               params['ref_filename'] + "HetOutliersClean")
    
    file = file[~file['ID'].isin(list(ref_remove['X.IID']))]

except FileNotFoundError:
    pass

try:
    own_remove = pd.read_table("results/1_QualityCheck/8_Heterozygosity/8.4_" +
                               params['own_filename'] + "HetOutliersClean")
    
    file = file[~file['ID'].isin(list(own_remove['X.IID']))]
except FileNotFoundError:
    pass

file.to_csv("results/FilteredPop.csv", index = None)

sample_list = file['ID']

sample_list.to_csv('results/SampleList.txt', index = None , header = None)