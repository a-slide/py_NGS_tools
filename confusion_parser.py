from collections import OrderedDict
import pysam
import glob

def distrib_bam (basename):
    bam_list = [name for name in glob.glob("*.bam")]
    bam_list.sort()
    with open (basename+"_confusion.csv", "wb") as out:
        out.write(" \tAAV\tBackbone\tHelper\tAd5\tPhage\tHuman\tUnmapped\tTotal\n")
        for bam in bam_list:
            print ("Processing file {}".format(bam))
            res = distrib_per_file(bam)
            print res
            out.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(
                bam,
                res['AAV'],
                res['backbone'],
                res['Helper'],
                res['Ad5'],
                res['Phage'],
                res['Human'],
                res['unmapped'],
		sum(res.values())))

def distrib_per_file (file):
    ref_dict = seq_dict=OrderedDict()
    ref_dict ['AAV'] = {'count':0, "seq":['Cassette-AAV-CMV-GFP-hTK',]}
    ref_dict ['backbone'] = {'count':0, "seq":['Backbone-AAV-CMV-GFP-hTK',]}
    ref_dict ['Helper'] = {'count':0, "seq":['pDP8_Kana',]}
    ref_dict ['Ad5'] = {'count':0, "seq":['Ad5_in_293_genome',]}
    ref_dict ['Phage'] = {'count':0, "seq":['Phage_lambda_genome_J02459.1',]}
    ref_dict ['Human'] = {'count':0, "seq":['1','10','11','12','13','14','15','16','17','18','19','2','20','21','22','3','4','5','6','7','8','9','MT','X','Y','KI270728.1','KI270727.1','KI270442.1','KI270729.1','GL000225.1','KI270743.1','GL000008.2','GL000009.2','KI270747.1','KI270722.1','GL000194.1','KI270742.1','GL000205.2','GL000195.1','KI270736.1','KI270733.1','GL000224.1','GL000219.1','KI270719.1','GL000216.2','KI270712.1','KI270706.1','KI270725.1','KI270744.1','KI270734.1','GL000213.1','GL000220.1','KI270715.1','GL000218.1','KI270749.1','KI270741.1','GL000221.1','KI270716.1','KI270731.1','KI270751.1','KI270750.1','KI270519.1','GL000214.1','KI270708.1','KI270730.1','KI270438.1','KI270737.1','KI270721.1','KI270738.1','KI270748.1','KI270435.1','GL000208.1','KI270538.1','KI270756.1','KI270739.1','KI270757.1','KI270709.1','KI270746.1','KI270753.1','KI270589.1','KI270726.1','KI270735.1','KI270711.1','KI270745.1','KI270714.1','KI270732.1','KI270713.1','KI270754.1','KI270710.1','KI270717.1','KI270724.1','KI270720.1','KI270723.1','KI270718.1','KI270317.1','KI270740.1','KI270755.1','KI270707.1','KI270579.1','KI270752.1','KI270512.1','KI270322.1','GL000226.1','KI270311.1','KI270366.1','KI270511.1','KI270448.1','KI270521.1','KI270581.1','KI270582.1','KI270515.1','KI270588.1','KI270591.1','KI270522.1','KI270507.1','KI270590.1','KI270584.1','KI270320.1','KI270382.1','KI270468.1','KI270467.1','KI270362.1','KI270517.1','KI270593.1','KI270528.1','KI270587.1','KI270364.1','KI270371.1','KI270333.1','KI270374.1','KI270411.1','KI270414.1','KI270510.1','KI270390.1','KI270375.1','KI270420.1','KI270509.1','KI270315.1','KI270302.1','KI270518.1','KI270530.1','KI270304.1','KI270418.1','KI270424.1','KI270417.1','KI270508.1','KI270303.1','KI270381.1','KI270529.1','KI270425.1','KI270396.1','KI270363.1','KI270386.1','KI270465.1','KI270383.1','KI270384.1','KI270330.1','KI270372.1','KI270548.1','KI270580.1','KI270387.1','KI270391.1','KI270305.1','KI270373.1','KI270422.1','KI270316.1','KI270340.1','KI270338.1','KI270583.1','KI270334.1','KI270429.1','KI270393.1','KI270516.1','KI270389.1','KI270466.1','KI270388.1','KI270544.1','KI270310.1','KI270412.1','KI270395.1','KI270376.1','KI270337.1','KI270335.1','KI270378.1','KI270379.1','KI270329.1','KI270419.1','KI270336.1','KI270312.1','KI270539.1','KI270385.1','KI270423.1','KI270392.1','KI270394.1']}
    ref_dict ['unmapped'] = {'count':0, "seq":['random_reference']}
    
    with pysam.Samfile(file, "rb" ) as bam:
        for read in bam:
            qname = read.qname.partition("_")[2].rpartition(":")[0]
	    if not qname:
		qname = read.qname.partition("_")[2]
            for ref in ref_dict.values():
                if qname in ref["seq"]:
                    ref["count"] +=1
    return {name:val['count']for name, val in ref_dict.items()}
