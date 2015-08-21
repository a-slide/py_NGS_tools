import pysam

def fetch_read(bam_file, seq_name, start, end):
    bam = pysam.AlignmentFile(bam_file, "rb")
    n = 0
    for i in bam.fetch(seq_name, start, end):
        n += 1
    return n
    
