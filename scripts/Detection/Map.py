#!/usr/bin/env python

''' 
 * All rights Reserved, Designed By HIT-Bioinformatics   
 * @Title:  Map.py
 * @Package: argparse, sys, os, logging
 * @Description: Classify the ME types
  * @author: Jiang Tao (tjiang@hit.edu.cn)
 * @date: Apr 24 2018
 * @version V1.0.2
'''

import os
import argparse
import logging
import tempfile
import sys, time
from CommandRunner import *

VERSION="1.0"

USAGE="""\
	Realignment of chimeric read parts.

	Aligner: NGMLR version 0.2.6
	TE refs: Alu families
		 L1 families
		 SVA families
	The output of this script is a .sam file.
"""

def call_ngmlr(inFile, ref, presets, nproc, outFile, SUBREAD_LENGTH, SUBREAD_CORRIDOR):
	"""
	fq = input file
	automatically search for .sa
	"""
	outFile = outFile + "cluster.sam"
	logging.info("Running NGMLR...")
	cmd = ("ngmlr -r %s -q %s -o %s -t %d -x %s --subread-length %d --subread-corridor %d" \
		% (ref, inFile, outFile, nproc, presets, SUBREAD_LENGTH, SUBREAD_CORRIDOR))
	r, o, e = exe(cmd)
	
	if r != 0:
		logging.error("NGMLR mapping failed!")
		logging.error("RETCODE %d" % (r))
		logging.error("STDOUT %s" % (str(o)))
		logging.error("STDERR %s" % (str(e)))
		logging.error("Exiting")
		exit(r)
	
	logging.info("Finished NGMLR mapping.")
	return outFile

def parseArgs(argv):
	parser = argparse.ArgumentParser(prog="process.py realignment", description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
	# parser.add_argument("AlignmentFile", type=str, help="the bam format file generated by ngmlr, within a '.bai' index file")
	parser.add_argument("input", metavar="FASTA", type=str, help="Input potential_ME.fa.")
	parser.add_argument("ME_Ref", type=str, help="The reference genome(fasta format).")
	parser.add_argument('output', type=str, help = "Prefix of potential ME classification.")
	# parser.add_argument("--temp", type=str, default=tempfile.gettempdir(), help="Where to save temporary files")

	# parser.add_argument('-s', '--min_support', help = "Mininum number of reads that support a TE.[%(default)s]", default = 5, type = int)
	# parser.add_argument('-l', '--min_length', help = "Mininum length of TE to be reported.[%(default)s]", default = 50, type = int)
	# parser.add_argument('-d', '--min_distance', help = "Mininum distance of two TE clusters.[%(default)s]", default = 20, type = int)
	# parser.add_argument('-hom', '--homozygous', help = "The mininum score of a genotyping reported as a homozygous.[%(default)s]", default = 0.8, type = float)
	# parser.add_argument('-het','--heterozygous', help = "The mininum score of a genotyping reported as a heterozygous.[%(default)s]", default = 0.3, type = float)
	# parser.add_argument('-q', '--min_mapq', help = "Mininum mapping quality.[20]", default = 20, type = int)
	parser.add_argument('-t', '--threads', help = "Number of threads to use.[%(default)s]", default = 8, type = int)
	parser.add_argument('-x', '--presets', help = "The sequencing platform <pacbio,ont> of the reads.[%(default)s]", default = "pacbio", type = str)
	parser.add_argument('--subread_length', help = "Length of fragments reads are split into [%(default)s]", default = 128, type = int)
	parser.add_argument('--subread_corridor', help = "Length of corridor sub-reads are aligned with [%(default)s]", default = 20, type = int)
	# parser.add_argument("--temp", type=str, default=tempfile.gettempdir(), help="Where to save temporary files")
	# parser.add_argument("--chunks", type=int, default=0, help="Create N scripts containing commands to each input of the fofn (%(default)s)")
	# parser.add_argument("--debug", action="store_true")
	args = parser.parse_args(argv)

	# setupLogging(args.debug)
	# checkBlasrParams(args.params)
	
	# if args.output is None:
	# 	ext =  args.input[args.input.rindex('.'):]
	# 	main = args.input[:args.input.rindex('.')]
	# 	if ext in [".sam", ".bam"]:
	# 		args.output = main + ".tails" + ext
	# 	else:
	# 		args.output = main + ".tails.sam"
	return args

def run(argv):
	args = parseArgs(argv)
	setupLogging(False)
	# print args
	starttime = time.time()
	call_ngmlr(args.input, args.ME_Ref, args.presets, args.threads, args.output, args.subread_length, args.subread_corridor)
	logging.info("Finished in %0.2f seconds."%(time.time() - starttime))

if __name__ == '__main__':
    run(sys.argv[:1])
