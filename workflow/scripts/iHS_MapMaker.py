#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 16:32:13 2022

@author: cbr
"""

import gzip 
import sys
import getopt

if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["input=", "output="]
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

        elif opt in ["--input"]:
            params['inputfile'] = arg

        elif opt in ["--output"]:
            params['outputfile'] = arg

    with open(params['outputfile'] , 'w') as out_file:
        with gzip.open(params['inputfile'] , 'r') as in_file:
            while True:
                line = in_file.readline().decode("UTF-8")
                
                if not line:
                    break
                
                
                if line[0:1] == '#':
                    continue
                
                else:
                    line_list = line.split()
                    out_file.write(line_list[0] + '\t' + line_list[2] + '\t' + line_list[1] + '\t' + line_list[1] + '\n')
