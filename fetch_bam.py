#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv as argv

from

""" Draft function to summarize the coverage over a ref in multiple bed files created by Contavect
in a single comprehensive csv file"""

def main ():
    """Find bed files with a common pattern fetch the 2nd row of the first alphabetical
    file and the 4rth row of all files. Merge everything in a common csv file
    Create a additional """

    # Find ref matching the patern and sorting the list alphabetically
    ref = list(glob.iglob("*"+argv[1]))
    ref.sort()
    print (ref)

    # Fetch second column (ref position)
    with open(ref[0], newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # Get rid of the bed header
        title = next(reader)

        # Fetch the position row and store it in 2 list for raw count and norm count
        pos_row = [row[1] for row in reader]
        all_count = [["", "Position"] + pos_row]
        all_norm =  [["", "Position"] + pos_row]



    # Fuse count and norm count tables and transpose the table
    all_data = all_count+all_norm
    all_data = [[x[i] for x in all_data] for i in range(len(all_data[0]))]

    # Finally write a new table
    with open(argv[2], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in all_data:
            writer.writerow(i)

    print("done")

    exit (0)

def fetch_count_read (alignment_file, seq_name, start, end):
    """
    Count the number of read that are at least partly overlapping a specified chromosomic region
    @param alignment_file Path to a sam or a bam file
    @param seq_name Name of the sequence where read are to be aligned on
    @param start Start genomic coordinates of the area of alignment
    @param end End End genomic coordinates of the area of alignment
    """
    # Specific imports
    from pysam import AlignmentFile
    
    al = AlignmentFile(alignment_file, "rb")
    
    # Count read aligned at least partly on the specified region
    n = 0
    for i in al.fetch(seq_name, start, end):
        n += 1
    return n



def usage():
    """Simple usage function"""

    print ("Usage: ", argv[0], "<Pattern of bed files to match> <output name of the csv file>")
    print ("\tExample : ", argv[0], " .AAV.csv  ALL_AAV.csv")
    exit(1)

if __name__ == '__main__':
    if len(argv) <= 2:        # if not enough arg call usage function
        usage()
    else:
        main()              # else call the main function
