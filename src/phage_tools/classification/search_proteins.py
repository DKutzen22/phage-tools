from phage_tools.classification.classify_genbank import genbank_classification
import phage_tools.local.keywords as keywords
import phage_tools.local.phages as phages

def search_proteins(accession_num, keyword_list):
    phage = genbank_classification(accession_num)
    matching_proteins = {}
    
    for protein_id, protein in phage.proteins.items():
        if any(keyword.lower() in (protein.product or "").lower() for keyword in keyword_list):
            matching_proteins[protein_id] = protein
    
    return phage, matching_proteins

