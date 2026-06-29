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
        start_pos = int(feature.location.start)
        stop_pos = int(feature.location.end)
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
        name = " ".join(seqrecord.features[0].qualifiers.get("organism", "blank")),
        accession = accession_num,
        taxonomy = ", ".join(seqrecord.annotations.get("taxonomy", None)),
        host = " ".join((seqrecord.features[0].qualifiers.get("host", None))),
        genome_size = len(sequence),
        proteins = proteins
    )
    
    return phage