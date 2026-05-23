from Bio import Entrez, SeqIO
import xlsxwriter
import re

Entrez.email = input("What is your NCBI email?")
Entrez.tool = "genbank_phage_genome"
genbank_id = input("What is the Phages Genbank ID Number?")



#retrieves genome data from NCBI GenBank
def genome_scraping(accession_num):
    
    #fetches the genbank data from the nucleotide database for the provided 'accession_num'
    with Entrez.efetch(db="nucleotide", 
                        id=accession_num, 
                        rettype="gb", 
                        retmode="text") as handle:

        #saves the data retrieved from genbank as a seqrecord
        record = SeqIO.read(handle, "genbank")

    return record



#organizes the reference genome into a dictionary with relevant features
def protein_scraping(accession_num):

    genome = genome_scraping(accession_num)

    proteins = {}
    
    #counter to verify the amount of proteins in the finished dictionary is correct
    cds_count = 0

    for feature in genome.features:

        #checks that the feature is a protein coding sequence
        if feature.type != "CDS": continue
        cds_count += 1

        #labels the feature, its name, and sequence
        gp = feature.qualifiers.get("note", "blank")[0].split(";")[0]
        product = feature.qualifiers.get("product", "blank")[0]
        translation = feature.qualifiers.get("translation", "blank")[0]
        
        #if the feature doesn't have a note, it labels with locus_tag instead
        if gp == "b":
            gp = feature.qualifiers.get("locus_tag")[0]

        #places the feature in the 'proteins' dictionary with its name and sequence 
        #organized by 'gp' to avoid duplication of keys
        proteins[gp] = {"Product":product, "Translation":translation}

        if cds_count != len(proteins):
            print("Error: Not all proteins were sorted correctly")

    return proteins



#create a function to retrieve all general data about the organism
def organism_scraping(accession_num):

    genome = genome_scraping(accession_num)

    description = {}

    for feature in genome.features:
        if feature.type == "source":
    
            description["Organism"] = feature.qualifiers.get("organism", "blank")[0]
            description["Host"] = feature.qualifiers.get("lab_host", "blank")[0]
            description["Isolation Source"] = feature.qualifiers.get("isolation_source", "blank")[0]
            description["Identified by"] = feature.qualifiers.get("identified_by", "blank")[0]
            description["Location"] = feature.qualifiers.get("geo_loc_name", "blank")[0]

    return description



#create a function that organizes the proteins by type
def protein_sorting(accession_num):

    proteins = protein_scraping(accession_num)

    #nested dictionary for sorting proteins into various classes
    sorted_proteins = {
        "capsid": {},
        "tail": {},
        "lysin": {},
        "holin": {},
        "spanin": {},
        "toxin": {},
        "integrase": {},
        "hypothetical": {},
        "others": {},
    }

    #regex patterns for sorting
    capsid = re.compile(r"\bhead\b|\bcapsid\b|\bcoat\b")
    tail = re.compile(r"tail")
    lysins = re.compile(r"lysin|lysozyme")
    holins = re.compile(r"holin")
    spanins = re.compile(r"spanin")
    toxins = re.compile(r"toxin|virulence")
    integrases = re.compile(r"integrase")
    superinfection = re.compile(r"superinfection")
    assembly = re.compile(r"assembly|prohead")
    portal = re.compile(r"connector|portal")
    hypothetical = re.compile(r"\bhypothetical\sprotein\b")

    #iterates through proteins for sorting
    for protein in proteins:

        #retrieves the protein product and translation data stored in 'proteins'
        product = proteins.get(protein).get("Product")
        translation = proteins.get(protein).get("Translation")
        
        #sorts proteins based on regex pattern matching, 
        #then adds each protein to the corresponding sub-dictionary in 'sorted_proteins'
        #starting with any proteins including 'hypohetical'
        if bool(hypothetical.search(product)):
            sorted_proteins["hypothetical"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'portal' or 'connector' into 'portal' sub-dictionary of 'sorted_proteins'
        elif bool(portal.search(product)):
            sorted_proteins["others"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'assembly' or 'prohead' into 'assembly' sub-dictionary of 'sorted_proteins'     
        elif bool(assembly.search(product)):
            sorted_proteins["others"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'superinfection' into 'superinfection' sub-dictionary of 'sorted_proteins'
        elif bool(superinfection.search(product)):
            sorted_proteins["others"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'integrase' into 'integrase' sub-dictionary of 'sorted_proteins'
        elif bool(integrases.search(product)):
            sorted_proteins["integrase"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'toxin' or 'virulence' into 'toxin' sub-dictionary of 'sorted_proteins'
        elif bool(toxins.search(product)):
            sorted_proteins["toxin"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'spanin' into 'spanin' sub-dictionary of 'sorted_proteins'
        elif bool(spanins.search(product)):
            sorted_proteins["spanin"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'holin' into 'holin' sub-dictionary of 'sorted_proteins'
        elif bool(holins.search(product)):
            sorted_proteins["holin"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'lysin' or 'lysozyme' into 'lysin' sub-dictionary of 'sorted_proteins'
        elif bool(lysins.search(product)):
            sorted_proteins["lysin"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'tail' into 'tail' sub-dictionary of 'sorted_proteins'
        elif bool(tail.search(product)):
            sorted_proteins["tail"][protein] = {"Product":product, "Translation":translation}
        #sorts proteins containing 'head', 'capsid', or 'coat' into 'capsid' sub-dictionary of 'sorted_proteins'
        elif bool(capsid.search(product)):
            sorted_proteins["capsid"][protein] = {"Product":product, "Translation":translation}
        #sorts remaining proteins into 'others' sub-dictionary of 'sorted_proteins'
        else: sorted_proteins["others"][protein] = {"Product":product, "Translation":translation}

    return sorted_proteins



#make an xlsx with a main info page and various other pages organized by type of protein
def xlsx_writer(accession_num_x):

    #retrieves the organism data and proteins
    organism_data = organism_scraping(accession_num_x)
    sorted_proteins = protein_sorting(accession_num_x)

    #creates an Excel workbook named using the organism name and ID
    workbook = xlsxwriter.Workbook(f"{accession_num_x} - {organism_data.get("Organism")}.xlsx")

    #creates a 'Description' worksheet populated with the organism data
    description = workbook.add_worksheet("Description")
    row = 0
    col = 0
    #iterates through the organism data, adding it row by row
    for key in organism_data:
        value = organism_data.get(key)
        description.write(row, col, key)
        description.write(row, col + 1, value)
        row += 1
    description.autofit()
    
    #creates a 'Capsid' worksheet populated with putative capsid proteins
    capsid = workbook.add_worksheet("Capsid")
    row = 0
    col = 0
    #iterates through the proteins, adding their name, product, and translation row by row
    for key in sorted_proteins["capsid"]:
        product = sorted_proteins.get("capsid").get(key).get("Product")
        translation = sorted_proteins.get("capsid").get(key).get("Translation")
        capsid.write(row, col, key)
        capsid.write(row, col + 1, product)
        capsid.write(row, col + 2, translation)
        row += 1
    capsid.autofit()
    
    #creates a 'Tail' worksheet populated with putative tail proteins
    tail = workbook.add_worksheet("Tail")
    row = 0
    col = 0
     #iterates through the proteins, adding their name, product, and translation row by row
    for key in sorted_proteins["tail"]:
        product = sorted_proteins.get("tail").get(key).get("Product")
        translation = sorted_proteins.get("tail").get(key).get("Translation")
        tail.write(row, col, key)
        tail.write(row, col + 1, product)
        tail.write(row, col + 2, translation)
        row += 1
    tail.autofit()
    
    if any(sorted_proteins.get("lysin").values()):
        #creates a 'Lysin' worksheet populated with putative lysin proteins
        lysin = workbook.add_worksheet("Lysin")
        row = 0
        col = 0
        #iterates through the proteins, adding their name, product, and translation row by row
        for key in sorted_proteins["lysin"]:
            product = sorted_proteins.get("lysin").get(key).get("Product")
            translation = sorted_proteins.get("lysin").get(key).get("Translation")
            lysin.write(row, col, key)
            lysin.write(row, col + 1, product)
            lysin.write(row, col + 2, translation)
            row += 1
        lysin.autofit()
    
    if any(sorted_proteins.get("holin").values()):
        #creates a 'Holin' worksheet populated with putative holin proteins
        holin = workbook.add_worksheet("Holin")
        row = 0
        col = 0
        #iterates through the proteins, adding their name, product, and translation row by row
        for key in sorted_proteins["holin"]:
            product = sorted_proteins.get("holin").get(key).get("Product")
            translation = sorted_proteins.get("holin").get(key).get("Translation")
            holin.write(row, col, key)
            holin.write(row, col + 1, product)
            holin.write(row, col + 2, translation)
            row += 1
        holin.autofit()
    
    if any(sorted_proteins.get("spanin").values()):
        #creates a 'Spanin' worksheet populated with putative spanin proteins
        spanin = workbook.add_worksheet("Spanin")
        row = 0
        col = 0
        #iterates through the proteins, adding their name, product, and translation row by row
        for key in sorted_proteins["spanin"]:
            product = sorted_proteins.get("spanin").get(key).get("Product")
            translation = sorted_proteins.get("spanin").get(key).get("Translation")
            spanin.write(row, col, key)
            spanin.write(row, col + 1, product)
            spanin.write(row, col + 2, translation)
            row += 1
        spanin.autofit()
    
    if any(sorted_proteins.get("toxin").values()):
        #creates a 'Toxin' worksheet populated with putative toxin proteins
        toxin = workbook.add_worksheet("Toxin")
        row = 0
        col = 0
        #iterates through the proteins, adding their name, product, and translation row by row
        for key in sorted_proteins["toxin"]:
            product = sorted_proteins.get("toxin").get(key).get("Product")
            translation = sorted_proteins.get("toxin").get(key).get("Translation")
            toxin.write(row, col, key)
            toxin.write(row, col + 1, product)
            toxin.write(row, col + 2, translation)
            row += 1
        toxin.autofit()
    
    if any(sorted_proteins.get("integrase").values()):
        #creates an 'Integrase' worksheet populated with putative integrase proteins
        integrase = workbook.add_worksheet("Integrase")
        row = 0
        col = 0
        #iterates through the proteins, adding their name, product, and translation row by row
        for key in sorted_proteins["integrase"]:
            product = sorted_proteins.get("integrase").get(key).get("Product")
            translation = sorted_proteins.get("integrase").get(key).get("Translation")
            integrase.write(row, col, key)
            integrase.write(row, col + 1, product)
            integrase.write(row, col + 2, translation)
            row += 1
        integrase.autofit()
    
    #creates an 'Others' worksheet populated with all other putative proteins that are not hypothetical
    others = workbook.add_worksheet("Others")
    row = 0
    col = 0
    #iterates through the proteins, adding their name, product, and translation row by row
    for key in sorted_proteins["others"]:
        product = sorted_proteins.get("others").get(key).get("Product")
        translation = sorted_proteins.get("others").get(key).get("Translation")
        others.write(row, col, key)
        others.write(row, col + 1, product)
        others.write(row, col + 2, translation)
        row += 1
    others.autofit()
    
    workbook.close()


xlsx_writer(genbank_id)
