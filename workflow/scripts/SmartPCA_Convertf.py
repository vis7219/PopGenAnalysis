#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:47:00 2022

@author: cbr
"""

import gzip 
import sys
import getopt


if __name__ == "__main__":
    argv = sys.argv[1:]
    smallflags = "K:"
    bigflags = ["input=", "type=", "output=", "location="]
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

        elif opt in ["--type"]:
            params['type'] = arg
            
        elif opt in ['--output']:
            params['output'] = arg
            
        elif opt in ['--location']:
            params['location'] = arg
            
    
    lines = ("genotypename:\t{input}.bed\n"\
            "snpname:\t{input}.pedsnp\n"\
            "indivname:\t{input}.pedind\n"\
            "outputformat:\t{type}\n"\
            "genooutfilename:\t{output}.eigenstratgeno\n"\
            "snpoutfilename:\t{output}.snp\n"\
            "indoutfilename:\t{output}.ind\n".format(input = params['input'],
                                                     type = params['type'],
                                                     output = params['output']))
        
    with open(str(params['location']) + "/2_par_Convert.txt" , 'w') as outfile:
        outfile.write(lines)