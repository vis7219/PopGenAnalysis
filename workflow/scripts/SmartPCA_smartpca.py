#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 14:43:17 2022

@author: cbr
"""

import gzip 
import sys
import getopt


if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["input=", "output=", "location=", "threads="]
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

        elif opt in ["--input"]:
            params['input'] = arg
            
        elif opt in ['--output']:
            params['output'] = arg
            
        elif opt in ['--location']:
            params['location'] = arg
            
        elif opt in ['--threads']:
            params['threads'] = arg
            
    
    lines = ("genotypename:\t{input}.eigenstratgeno\n"\
            "snpname:\t{input}.snp\n"\
            "indivname:\t{input}.ind\n"\
            "evecoutname:\t{output}.evec\n"\
            "evaloutname:\t{output}.eval\n"\
            "numthreads:\t{threads}".format(input = params['input'],
                                            output = params['output'],
                                            threads = params['threads']))
        
    with open(str(params['location']) + "/3_par_SmartPCA.txt" , 'w') as outfile:
        outfile.write(lines)