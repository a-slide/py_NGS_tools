#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import glob
from collections import OrderedDict
from pprint import pprint 

def main():
    
    # Empty report list 
    r = []
    
    file_list = glob.glob("./*/fastqc_data.txt")
    assert file_list, "No file fastqc_data.txt found"

    for f_path in file_list:
        with open (f_path, "r") as f:
            
            Quality_module = Overrepresented_sequences = Kmer_Content = False
            qual_score = n_overrepresented_seq = n_kmer = 0
            
            d = OrderedDict()
            
            for line in f:
                if line.startswith("Filename"):
                    d["Sample Name"] = line.split("\t")[1].strip()
                elif line.startswith("Total Sequences"):
                    d["Total Sequences"] = int(line.split("\t")[1].strip())
                elif line.startswith("%GC"):
                    d["%GC"] = int(line.split("\t")[1].strip())
                elif line.startswith("#Total Duplicate Percentage"):
                    d["Duplicate Percentage"] = round(float(line.split("\t")[1].strip()), 2)
                
                # Found first line and last line of specific modules
                elif line == ">>END_MODULE\n":
                    Quality_module = Overrepresented_sequences = Kmer_Content = False
                elif line == "#Quality\tCount\n":
                    Quality_module = True
                elif line == "#Sequence\tCount\tPercentage\tPossible Source\n":
                    Overrepresented_sequences = True
                elif line == "#Sequence\tCount\tObs/Exp Overall\tObs/Exp Max\tMax Obs/Exp Position\n":
                    Kmer_Content = True
                
                # Specific data extraction in modules 
                elif Quality_module:
                    qual_score += int(line.split("\t")[0].strip()) * float(line.split("\t")[1].strip())
                elif Overrepresented_sequences:
                    n_overrepresented_seq+=1
                elif Kmer_Content:
                    n_kmer+=1
            
            d["Mean quality"] = round(qual_score / d["Total Sequences"], 2)
            d["Number of overrepresented sequences"] = n_overrepresented_seq
            d["Number of overrepresented Kmers"] = n_kmer            
            r.append(d)
    
    with open ("Summary_reports.csv", "w") as report:
        report.write("\t".join(r[0].keys())+"\n")
        for i in r:
            report.write("\t".join([str(val) for val in i.values()])+"\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   TOP LEVEL INSTRUCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':

    main()
