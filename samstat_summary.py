#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import glob
from collections import OrderedDict

def main():
    
    # Empty report list 
    r = []
    
    file_list = glob.glob("./*samstat.html")
    assert file_list, "No file samstat.html report found"

    for f_path in file_list:
        with open (f_path, "r") as f:
            
            d = OrderedDict()
            
            found = False
            tag_name = None
            
            for line in f:
                
                # Find sample name
                if line.startswith("""<title>"""):
                    d["Sample name"] = line.rpartition("<")[0].partition(">")[-1]
                
                # Find the quality counts in the html tables
                if line ==  """<table  class="simple" >\n""":
                    found = True
                elif line == """</table>\n""":
                    found = False
                elif found:
                    if line.startswith("""<td style="background-color:"""):
                        tag_name = line.rpartition("<")[0].partition(">")[-1]
                    elif tag_name:
                        value = float(line.rpartition("<")[0].partition(">")[-1])
                        d[tag_name] = value
                        tag_name = None
       
            r.append(d)
    
    with open ("samstat_summary_reports.csv", "w") as report:
        report.write("\t".join(r[0].keys())+"\n")
        for i in r:
            report.write("\t".join([str(val) for val in i.values()])+"\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   TOP LEVEL INSTRUCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':

    main()
