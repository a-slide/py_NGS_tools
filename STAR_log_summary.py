#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import glob
from collections import OrderedDict

def main():
    
    # Empty report list 
    r = []
    
    file_list = glob.glob("./*Log.final.out")
    assert file_list, "No file STAR Log.final.out found"

    for f_path in file_list:
        with open (f_path, "r") as f:
            d = OrderedDict()
            d["Sample Name"] = f_path[:-14].rpartition("/")[-1]
        
            for line in f:
                for attribute_name in [
                    "Number of input reads",
                    "Average input read length",
                    "Uniquely mapped reads number",
                    "Uniquely mapped reads %",
                    "Average mapped length",
                    "Number of splices: Total",
                    "Number of splices: Annotated (sjdb)",
                    "Number of splices: GT/AG",
                    "Number of splices: GC/AG",
                    "Number of splices: AT/AC",
                    "Number of splices: Non-canonical",
                    "Mismatch rate per base, %",
                    "Deletion rate per base",
                    "Deletion average length",
                    "Insertion rate per base",
                    "Insertion average length",
                    "Number of reads mapped to multiple loci",
                    "% of reads mapped to multiple loci",
                    "Number of reads mapped to too many loci",
                    "% of reads mapped to too many loci",
                    "% of reads unmapped: too many mismatches",
                    "% of reads unmapped: too short",
                    "% of reads unmapped: other"] :
                
                    # loop until the end or as soon as a attribute name is found
                    if line.strip().startswith(attribute_name):
                        d[attribute_name] = line.split("|")[1].strip()
                        break
                
            r.append(d)
    
    with open ("STAR_summary_reports.csv", "w") as report:
        report.write("\t".join(r[0].keys())+"\n")
        for i in r:
            report.write("\t".join([str(val) for val in i.values()])+"\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   TOP LEVEL INSTRUCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':

    main()
