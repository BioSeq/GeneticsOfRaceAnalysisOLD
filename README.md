These scripts automate the analysis of the data of the Genetics of Race project
for the BioSeq project. The use a config file that is specified in the
genRaceAnalysis.py script. The join2Fastas2.py script is used by the
aforementioned script as a helper procedure. A sample config file is included.
It has several fake entries to demonstrate that the program can handle bad
input.

Author: Philip Braunstein
Contact: pbraunstein12@gmail.com

===========
CONFIG FILE
==========
 This script uses a CONFIG file that specifies that lists the HVRI
 vcf file then the HVRII vcf file from the same sample on each line.
 The names on each line are comma-speparated. Each name is listed without
 the .vcf extension. So, if the vcf file is S501N703_S11.vcf, the CONFIG
 file lists this as S501N703_S11.

 The path to the CONFIG file is specified in the CONFIG constant at the top of
 this file.

=============
DEPENDENCIES
============
    1. Path to the GATK jar file must be in the GATK constant. It is easiest
       to have a sym link in the directory.
    2. Path to the join script must be specifed in the genRaceAnalysis.py. 
       Likewise, it is easiest to have this script in the same directory.

