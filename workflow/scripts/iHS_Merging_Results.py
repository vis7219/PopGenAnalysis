#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:39:22 2022

@author: cbr
"""

import gzip 
import sys
import getopt
import pandas as pd

if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["input_pop=", "bins=", "chromosome="]
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
            
        elif opt in ["--chromosome"]:
            params['chromosome'] = arg


new_df = pd.DataFrame(columns = ['SNP ID' , 'pos' , 'ihs' , 'normihs' , 'Chr' , 'ABS_normihs'])

for i in range(1,int(params['chromosome']) + 1):
    df = pd.read_table(params['inputpop'] + ".chr" +
                       str (i) + "_iHS.Result.ihs.out." + params['bins'] + "bins.norm",
                       header = None)
    df.drop([2,3,4,7],axis = 1, inplace = True)
    df['Chr'] = i
    df.rename({0 : 'SNP ID',
               1 : 'pos',
               5 : 'ihs',
               6 : 'normihs'}, inplace = True, axis = 1)
    df['ABS_normihs'] = abs(df['normihs'])
    
    new_df = pd.concat([new_df , df])
    
new_df.to_csv(params['inputpop'] + "_iHS_Complete.norm" , sep = '\t', index = None)

