#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import glob
from collections import OrderedDict
import pysam

def main():
       
    file_list = glob.glob("./*bam")
    assert file_list, "No bam file found"
    report_name = "mapping_summary_reports.csv"

    with open (report_name, "w") as report:
        report.write("Summary of count per reference\n\n")
    
    for f_path in file_list:
        basename = f_path.rpartition("/")[-1].partition(".")[0]
        report_dict = OrderedDict()
        report_dict["secondary"] = 0
        report_dict["unmapped"] = 0
        report_dict["low_mapq"] = 0
        
        print ("\nProcessing sample "+basename)
        
        with pysam.AlignmentFile(f_path, "rb") as bam:
            for read in bam:            

                if read.is_secondary:
                    report_dict["secondary"] += 1
                
                elif read.is_unmapped:
                    report_dict["unmapped"] += 1
                
                elif read.mapping_quality < 30:
                    report_dict["low_mapq"] += 1

                else:
                    ref_name = bam.getrname(read.tid)
                    if not ref_name in report_dict:
                        report_dict[ref_name] = 0
                    report_dict[ref_name] += 1
            
            for i, j in report_dict.items():
                print ("\tCount {} = {}".format(i, j))
            
            with open (report_name, "a") as report:
                report.write("\t{}\n".format("\t".join(report_dict.keys())))
                report.write("{}\t{}\n".format(basename, "\t".join([str(val) for val in report_dict.values()])))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   TOP LEVEL INSTRUCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':

    main()
