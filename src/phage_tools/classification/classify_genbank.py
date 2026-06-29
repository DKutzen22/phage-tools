from phage_tools.io.genbank_io import genome_scraping
from phage_tools.modules.classes import Protein, Phage
import re


def genbank_classification(accession_num):
    seqrecord = genome_scraping(accession_num)
    sequence = seqrecord.seq
    proteins = {}

    for feature in seqrecord.features:

        if feature.type != "CDS": continue

        gp = feature.qualifiers.get("note", "blank")[0].split(";")[0]
        product = feature.qualifiers.get("product", "blank")[0]
        translation = feature.qualifiers.get("translation", "blank")[0]


        start_pos = feature.location.start
        stop_pos = feature.location.end
        gene_sequence = str(sequence[start_pos:stop_pos])

        if not re.search(r"^gp.*", gp):
            gp = feature.qualifiers.get("locus_tag")[0]


        proteins[gp] = Protein(
            id=gp,
            translation=translation,
            locus_tag=feature.qualifiers.get("locus_tag", [None])[0],
            product=product,
            start=start_pos,
            stop=stop_pos,
            sequence=gene_sequence
        )

    phage = Phage(
        name = seqrecord.features[0].qualifiers.get("organism", "blank")[0],
        accession = accession_num,
        taxonomy = seqrecord.annotations.get("taxonomy", "blank"),
        proteins = proteins
    )
    return phage

print(genbank_classification("NC_001416.1"))

#retrieves general organism data from the genome
def organism_scraping(accession_num):
    #retrieves the genome and creates a filler re.pattern for 'Description'
    seqrecord = genome_scraping(accession_num)
    Description_pattern = re.compile(r"supercalifragilisticexpialidocious")
    #dict for various relevant facts about the organism
    description = {
        "pattern": Description_pattern,
        "Organism": {},
        "Host": {},
        "Isolation Source": {},
        "Identified by": {},
        "Location": {}
    }
    #retrieves the organism data and adds it to the 'description' dict
    for feature in seqrecord.features:
        if feature.type == "source":
            description["Organism"]["Product"] = feature.qualifiers.get("organism", "blank")[0]
            description["Host"]["Product"] = feature.qualifiers.get("lab_host", "blank")[0]
            description["Isolation Source"]["Product"] = feature.qualifiers.get("isolation_source", "blank")[0]
            description["Identified by"]["Product"] = feature.qualifiers.get("identified_by", "blank")[0]
            description["Location"]["Product"] = feature.qualifiers.get("geo_loc_name", "blank")[0]

    return description
