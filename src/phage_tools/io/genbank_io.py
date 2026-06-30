from Bio import Entrez, SeqIO
import phage_tools.local.phages as phages

Entrez.email = "daltonkkutzen@gmail.com"
Entrez.tool = "genbank_scraper"

#retrieves genome data from NCBI GenBank
def genome_scraping(accession_num):
    #fetches the genbank data from the nucleotide database for the provided 'accession_num'
    with Entrez.efetch(db="nucleotide", 
                        id=accession_num, 
                        rettype="gb", 
                        retmode="text") as handle:
        #saves the data retrieved from genbank as a seqrecord
        seqrecord = SeqIO.read(handle, "genbank")

    return seqrecord
