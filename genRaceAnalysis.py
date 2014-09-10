#!/usr/bin/env python

#
# genRaceAnalysis.py
#
# Author: Philip Braunstein
# Scientist: Bridget Yang
#
# Date: May 8, 2014
# Last Modified: May 8, 2014
#
# SUMMARY
# This script makes FASTA files for each region in each sample using the
# FastaAlternateReferenceMaker then concatenates the sequence of the second
# sample onto the end of the sequence of the first sample. Paired regions are
# specified in the CONFIG file.
#
#
# CONFIG FILE
# This script uses a CONFIG file that specifies that lists the HVRI
# vcf file then the HVRII vcf file from the same sample on each line.
# The names on each line are comma-speparated. Each name is listed without
# the .vcf extension. So, if the vcf file is S501N703_S11.vcf, the CONFIG
# file lists this as S501N703_S11.
#
# The path to the CONFIG file is specified in the CONFIG constant at the top of
# this file.
#
#
# DEPENDENCIES
#    1. Path to the GATK jar file must be in the GATK constant. It is easiest
#       to have a sym link in the directory.
#    2. Path to the join script must be specifed in this script. Likewise,
#       it is easiest to have this script in the same directory.
#

# CONSTANTS
# Config file
CONFIG = "config1.txt"

# FASTA References
REFI = "HVRI.fasta"
REFII = "HVRII.fasta"

# GATK Parameters
PARAMS = "-Xmx2g"
GATK = "GenomeAnalysisTK.jar"
PROG = "FastaAlternateReferenceMaker"

# Script that appropriately concatenates the regions from each sample
JOIN_SCRIPT = "./join2Fastas2.py"

# For more convenient indexing into GATK arrays
OUT_INDEX = 9
VARIANT_INDEX = 11

import subprocess as sp
from sys import argv
import sys


# Checks is args are valid and prints error messages
# Exits if args not valid
def argsValid():
        valid = True  # Valid until known otherwise
        if len(argv) > 2:
                print "ERROR: Too many command line arguments"
                valid = False
        if len(argv) == 2:
                if argv[1] != '-v':
                        print "ERROR: Unknown argument:", argv[1]
                        valid = False

        if not valid:  # Print general error message about usage
                print "USAGE:", argv[0]
                print "Invoke with -v for GATK debug output"
                sys.exit(1)
        

# Returns True if debug output should be used, False otherwise
def verboseMode():
        if len(argv) == 1:
                return False

        if argv[1] == "-v":
                return True


# Reads in the config file into a dictionary so that
# the first entry is the key and the second entry is
# the value on each line.
# Expects config file to be comma separated with one
# entry per line.
def readInConfig():
        dictio = {}

        try:
                with open(CONFIG, 'r') as filer:
                        for line in filer:
                                listl = line.split(",")
                                listl = [x.strip() for x in listl]
                                dictio[listl[0]] = listl[1]
        except IOError:
                print "ERROR: Cannot find config file:", CONFIG
                sys.exit(2)

        return dictio

# Runs GATK PROG with REFI for every key in pairs
# and runs GATK PROG with REFII for every value in
# pairs.
# This function prints all of the GATK output
def generateFASTAsDebug(pairs):
        ref1 = ["java", PARAMS, "-jar", GATK, "-R", REFI, "-T", PROG, "-o", \
                        "PHOLDER", "--variant", "PHOLDER"]

        ref2 = ["java", PARAMS, "-jar", GATK, "-R", REFII, "-T", PROG, "-o", \
                        "PHOLDER", "--variant", "PHOLDER"]

        # Partition files into REFI and REFII
        odds = pairs.keys()
        evens = pairs.values()

        print "Generating FASTA Files...."

        # Run GATK for samples with REFI
        for sample in odds:
                ref1[OUT_INDEX] = sample + ".fasta"
                ref1[VARIANT_INDEX] = sample + ".vcf"

                print ref1[OUT_INDEX], "=>",

                code = sp.call(ref1)

                if code == 0:
                        print "success"
                else:
                        print "FAILED"
                

                

                
        # Run GATK for samples with REFII
        for sample in evens:
                ref2[OUT_INDEX] = sample + ".fasta"
                ref2[VARIANT_INDEX] = sample + ".vcf"

                print ref2[OUT_INDEX], "=>",

                code = sp.call(ref2)

                if code == 0:
                        print "success"
                else:
                        print "FAILED"



# Runs GATK PROG with REFI for every key in pairs
# and runs GATK PROG with REFII for every value in
# pairs.
# This function supresses all output from GATK.
def generateFASTAs(pairs):
        ref1 = ["java", PARAMS, "-jar", GATK, "-R", REFI, "-T", PROG, "-o", \
                        "PHOLDER", "--variant", "PHOLDER"]

        ref2 = ["java", PARAMS, "-jar", GATK, "-R", REFII, "-T", PROG, "-o", \
                        "PHOLDER", "--variant", "PHOLDER"]

        # Partition files into REFI and REFII
        odds = pairs.keys()
        evens = pairs.values()

        filew = open("/dev/null", "w")

        print "Generating FASTA Files...."

        # Run GATK for samples with REFI
        for sample in odds:
                ref1[OUT_INDEX] = sample + ".fasta"
                ref1[VARIANT_INDEX] = sample + ".vcf"

                print ref1[OUT_INDEX], "=>",

                code = sp.call(ref1, stdout=filew, stderr=filew)

                if code == 0:
                        print "success"
                else:
                        print "FAILED"

                
        # Run GATK for samples with REFII
        for sample in evens:
                ref2[OUT_INDEX] = sample + ".fasta"
                ref2[VARIANT_INDEX] = sample + ".vcf"

                print ref2[OUT_INDEX], "=>",

                code = sp.call(ref2, stdout=filew, stderr=filew) 

                if code == 0:
                        print "success"
                else:
                        print "FAILED"


        filew.close()


# Joins two FASTA files using the helper script 
def joinFASTAs(pairs):
        print "Joining FASTA Files...."
        
        firsts = pairs.keys()

        for sample in firsts:
                one = sample + ".fasta"
                two = pairs[sample] + ".fasta"
                process = [JOIN_SCRIPT, one, two]

                print "Joining", one, two, "=>",

                code = sp.call(process)

                if code == 0:
                        print "success"
                else:
                        print "FAILED"

                if code == 2:
                        print "ERROR: No such file"

        


def run():
        # Exits if command line arguments to script are not valid
        argsValid()

        # Get pairs info from config file
        pairs = readInConfig()

        if verboseMode():
                generateFASTAsDebug(pairs)
        else:
                generateFASTAs(pairs)

        joinFASTAs(pairs)

        sys.exit(0)

run()
