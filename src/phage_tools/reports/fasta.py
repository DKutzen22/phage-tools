from phage_tools.classification.search_proteins import search_proteins
from phage_tools.classification.classify_genbank import genbank_classification
import phage_tools.local.keywords as keywords
import phage_tools.local.phages as phages

def matching_proteins_fasta(accession_num, keyword_list):
    phage, matching_proteins = search_proteins(accession_num, keyword_list)
    fasta_output = ""
    
    for protein_id, protein in matching_proteins.items():
        fasta_output += f">{phage.name}_{protein.product}_{protein.locus_tag}_{phage.accession}\n{protein.translation}\n"
    
    return phage, fasta_output

def multi_phage_matching_fasta(phage_list, keyword_list):
    combined_output = ""

    for current_phage in phage_list:
        phage, fasta_output = matching_proteins_fasta(current_phage, keyword_list)
        combined_output += f">{phage.name}_{phage.accession}\n{fasta_output}"

    return combined_output

def write_fasta_to_file(phage_list, keyword_list, filename):
    fasta_output = multi_phage_matching_fasta(phage_list, keyword_list)

    with open("src/phage_tools/output/" + filename, "w") as fasta_file:
        fasta_file.write(fasta_output)

write_fasta_to_file(phages.maddie, keywords.tails, "maddie_tail_proteins.fasta")

print("done")

