#!/usr/bin/env python

#
# join2Fastas.py
#        
# Author: Philip Braunstein
# Scientist: Bridget Yang
#
# Date: April 1, 2014
# Last Modified: May 8, 2014
#
# A script that takes in two .fasta files from the
# command line and concatenates the sequence of the
# second .fasta file to the end of the first .fasta
# file in a new file.
#       
# This program eliminates any extraneous white space
# in the files.
#       
# Output file is named [FASTA1]_joined.fasta
# however the _S from the end of the name
# of the fasta file is stripped off.
#
# The header is named the same as the output file
# except with out the.fasta file extension.
#
# This script WILL NOT WORK if there are periods in the 
# file name.
#

# CONSTANTS
FILE_TYPE = "fasta"

# ERRORS
WRONG_FILE_ERROR = "Invalid file type provided on command line"
FORMAT_ERROR = ".fasta file is not formatted correctly"

from sys import argv
import sys

def usage(flag = "DEFAULT"):
        if flag == "DEFAULT":
                print "USAGE:", argv[0], "[FASTA_1] [FASTA_2]"
        else:
                print flag
        sys.exit(1)


def verifyInput():
        if len(argv) != 3:
                usage();

        # Verify file extension
        argList1 = argv[1].split(".")
        argList2 = argv[2].split(".")

        if len(argList1) != 2 or len(argList2) != 2:
                usage(WRONG_FILE_ERROR)

        if argList1[1] != FILE_TYPE or argList2[1] != FILE_TYPE:
                usage(WRONG_FILE_ERROR)


# Reads in a fasta file into a list -- stripping extraneous white space
# If the file doesn't start with ">", the function exits
def readIn(inFile):
        toReturn = []

        try:
                with open(inFile, 'r') as filer:
                        for line in filer:
                                line = line.strip()
                                toReturn.append(line)
        except IOError:
                sys.exit(2)

        if toReturn[0][0] != ">":
                usage(FORMAT_ERROR)
        
        return toReturn


# Writes combined fasta file by concatenating fileB to end of fileA.
def combineOutput(fileA, fileB):
        header = argv[1].split(".")[0]  # Get before extension first filename
        header = header.split("_")[0]  # Split off the _S tag no longer need
        fileName = header + "_joined." + FILE_TYPE

        with open(fileName, 'w') as filew:
                filew.write(">" + header + "\n")   # Write out header
                for lineA in fileA:
                        if lineA.startswith(">"):
                                continue  # Skip copy of the header
                        else:
                                filew.write(lineA)

                for lineB in fileB:
                        if lineB.startswith(">"):
                                continue  # Skip second copy of header
                        else:
                                filew.write(lineB)
                
def run():
        verifyInput()
       
        fileA = readIn(argv[1])
        fileB = readIn(argv[2])

        combineOutput(fileA, fileB)

        sys.exit(0)

run()

