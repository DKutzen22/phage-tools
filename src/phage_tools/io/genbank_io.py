from Bio import Entrez, SeqIO

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
        try:
            seqrecord = SeqIO.read(handle, "genbank")
        except ValueError as e:
            if str(e) == "No records found in handle":
                # handle the empty/mismatched file case
                print(f"No sequences found for {accession_num}; skipping.")
                seqrecord = None
            else:
                # re-raise other ValueErrors you didn't expect
                raise

    return seqrecord
