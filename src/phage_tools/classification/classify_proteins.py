from phage_tools.classification.classify_genbank import genbank_classification

def classify_proteins(accession_num):
    phage = genbank_classification(accession_num)
    
    return phage

