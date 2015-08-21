# -*- coding: utf-8 -*-

"""
@package    Sekator
@brief      Contain a class to model a fastq sequence and an iterator function to read fastq files
@copyright  [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)
@author     Adrien Leger - 2014
* <adrien.leger@gmail.com>
* <adrien.leger@inserm.fr>
* <adrien.leger@univ-nantes.fr>
* [Github](https://github.com/a-slide)
* [Atlantic Gene Therapies - INSERM 1089] (http://www.atlantic-gene-therapies.fr/)
"""

# Third party imports
import numpy as np

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class FastqSeq (object):
    """
    Simple Representation of a fastq file. The object support slicing and addition operations
    The quality score is a numpy array to facilitate further data manipulation
    Only works with illumina 1.8+ Phred +33 quality encoding
    """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


    #~~~~~~~FUNDAMENTAL METHODS~~~~~~~#

    def __init__ (self, sampleName, seq, qual, sampleIndex, molecularIndex):
        """
        @param sampleName Name of the sequence
        @param seq DNA sequence string
        @param qual string of quality encoded in illumina 1.8+ phred +33, or ndarray of int or
        list of int
        @param sampleIndex Index of the sample
        @param molecularIndex Index used to remove PCR duplicate
        """

        self.sampleName = sampleName
        self.seq = seq
        self.sampleIndex = sampleIndex
        self.molecularIndex = molecularIndex

        if type(qual) == str:
            self.qual = np.array([ord(x)-33 for x in qual])

        elif type(qual) == np.ndarray:
            self.qual = qual

        elif type(qual) == list:
            self.qual = np.array(qual)

        else:
            raise TypeError("qual is not a valid type : str, numpy.ndarray or list of int")

        assert len(self.seq) == len(self.qual), "Sequence length and quality string length are not equal."

    def __repr__(self):
        """Return a quick view of datas"""
        if len(self) > 20:
            return "Seq:{}\tSample index: {}\tMolecular index: {}\nSeq: {}...{}\nQual: {}...{}".format(self.sampleName, self.sampleIndex, self.molecularIndex, self.seq[:10], self.seq[-10:], self.qual[:10], self.qual[-10:])
        else:
            return "Seq:{}\tSample index: {}\tMolecular index: {}\nSeq: {}\nQual: {}".format(self.sampleName, self.sampleIndex, self.molecularIndex, self.seq, self.qual)

    def __str__(self):
        """Return string formated as a fastq sequence"""
        return "@{}:{}:{}\n{}\n+\n{}\n".format(self.sampleName, self.sampleIndex, self.molecularIndex, self.seq, self.qualstr)


    #~~~~~~~PROPERTIES~~~~~~~#

    @property
    def qualstr(self ):
        """Compute the quality string from the numpy int array """
        qualstr_phred = ""
        for i in self.qual:
            qualstr_phred += str(unichr(i+33))
        return qualstr_phred


    #~~~~~~~MAGIC METHODS~~~~~~~#

    def __len__ (self):
        """Support for len method"""
        return len(self.seq)

    def __getitem__( self, item ):
        """Support for slicing operator"""
        return FastqSeq(sampleName = self.sampleName, seq = self.seq[ item ], qual = self.qual[ item ])

    def __add__(self, other):
        """Support for concatenation of fastqSeq objects = + operator"""
        return FastqSeq(
            sampleName = "{}_{}".format(self.sampleName, other.name),
            seq = self.seq+other.seq,
            qual = np.concatenate((self.qual, other.qual)),
            descr = self.descr+other.descr)
