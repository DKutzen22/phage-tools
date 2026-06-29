from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Protein:
    id: str
    translation: str
    locus_tag: Optional[str] = None
    product: Optional[str] = "hypothetical protein"
    start: Optional[int] = None
    stop: Optional[int] = None
    sequence: Optional[str] = None

@dataclass
class Phage:
    name: str
    accession: Optional[str] = None
    taxonomy: Optional[str] = None
    host: Optional[str] = None
    genome_size: Optional[int] = None
    proteins: Dict[str, Protein] = field(default_factory=dict)
