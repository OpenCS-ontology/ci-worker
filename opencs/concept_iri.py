from functools import total_ordering
from rdflib import URIRef


@total_ordering
class ConceptIRI(URIRef):
    concept_id: int = 0

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: URIRef):
        if isinstance(other, ConceptIRI):
            return self.concept_id.__eq__(other.concept_id)
        else:
            return super().__eq__(other)

    def __gt__(self, other: URIRef):
        if isinstance(other, ConceptIRI):
            return self.concept_id.__gt__(other.concept_id)
        else:
            return super().__gt__(other)

    def __lt__(self, other: URIRef):
        if isinstance(other, ConceptIRI):
            return self.concept_id.__lt__(other.concept_id)
        else:
            return super().__lt__(other)
