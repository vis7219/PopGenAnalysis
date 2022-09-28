#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 11:23:57 2022

@author: cbr
"""

import gzip 
import sys
import getopt
import pandas as pd

if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["input_pop=", "bins=", "chromosome=", "input_refpop"]
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
            
        elif opt in ["--input_refpop"]:
             params['inputrefpop'] = arg
            
        elif opt in ["--bins"]:
            params['bins'] = arg
            
        elif opt in ["--chromosome"]:
            params['chromosome'] = arg

new_df = pd.DataFrame(columns = ['pos' , 'xpehh' , 'normxpehh'])

for i in range(1,params['chromosome'] + 1):
    df = pd.read_table(params['inputrefpop'] + "_" + params['inputpop'] +
                       ".chr" + str(i) + ".xpehh.out.norm")
    df.drop(['gpos' , 'p1' , 'ihh1' , 'p2' , 'crit', 'ihh2'],
            inplace = True,
            axis = 1)
    df['Chr'] = i
    
    new_df = pd.concat([new_df, df])
    
new_df.to_csv(params['inputrefpop'] + "_" + params['inputpop'] + ".Complete.xpehh.out.norm",
              sep = '\t')

