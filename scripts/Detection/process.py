#!/usr/bin/env python

''' 
 * All rights Reserved, Designed By HIT-Bioinformatics   
 * @Title:  process.py
 * @Package: argparse, pysam, sys
 * @Description: Control the nTED pipeline
 * @author: tjiang
 * @date: Apr 24 2018
 * @version V1.0     
'''

import argparse
import sys
import pysam
import extract, Map, call_TE
# from process import *

STAGES = {"detection": extract.run, \
          "realignment": Map.run, \
          "calling": call_TE.run}

VERSION="1.0.1"

USAGE = """\
           _  ___  _   _____   _______   _
     _ _  | ^_   _^ | |  ___| |__   __| | |
    | ^_| | | | | | | | |__      | |    | |
    | |   | | | | | | |  __|     | |    | |
    | |   | | | | | | | |___     | |    | |___
    |_|   |_| |_| |_| |_____|    |_|    |_____|

    rMETL - realignment-based Mobile Element insertion detection Tool for Long read

  STAGE is one of
    detection    Inference of putative MEI loci.
    realignment  Realignment of chimeric read parts.
    calling      Mobile Element Insertion calling.
    
  See README.md for documentation or --help for details
  
  rMETL V%s
"""%(VERSION)

def parseArgs():

	parser = argparse.ArgumentParser(prog="process.py", description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)

	# parser.add_argument("-h", "--help", action="store_true")
	parser.add_argument("stage", metavar="STAGE", choices=STAGES.keys(), type=str, help="Stage to execute")
	parser.add_argument("options", metavar="OPTIONS", nargs=argparse.REMAINDER, help="Options to pass to the stage")

	args = parser.parse_args()

	STAGES[args.stage](args.options)

if __name__ == '__main__':
	parseArgs()