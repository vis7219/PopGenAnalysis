#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 14:38:16 2022

@author: cbr
"""

import gzip 
import sys
import getopt
import pandas as pd

if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["file=", "poptype=", "pop=" , "output="]
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

        elif opt in ["--poptype"]:
            params['pop_type'] = arg
            
        elif opt in ["--pop"]:
            params['pop_name'] = arg
            
        elif opt in ['--output']:
            params['output'] = arg
            
file = pd.read_csv(params['file'])

pop_df = file[file[params['pop_type']] == params['pop_name']]

pop_list = pop_df['ID']

pop_list.to_csv(params['output'] + "PopulationList.txt",
                index = None,
                header = None)

ethnicity_list = pop_df['Pop']
ethnicity_list.to_csv(params['output'] + 'EthnicityList.txt',
                      index = None,
                      header = None)


