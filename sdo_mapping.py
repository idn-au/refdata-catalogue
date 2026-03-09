from pathlib import Path
from typing import TypedDict

from rdflib import Graph, URIRef, BNode, Namespace
from rdflib.namespace import DCAT, DCTERMS, SDO, PROV, RDF, RDFS, SKOS

REG = Namespace("http://purl.org/linked-data/registry#")

DIRECTORY = Path(__file__).parent / "vocabs/sync"
# DIRECTORY = Path(__file__).parent / "vocabs/non-sync"


class Mapping(TypedDict):
    key: list[URIRef]
    to: URIRef | tuple[URIRef]


type_mappings: list[Mapping] = [
    {
        "key": [DCAT.Catalog],
        "to": SDO.DataCatalog,
    },
    {
        "key": [DCAT.Dataset],
        "to": SDO.Dataset,
    },
    {
        "key": [DCAT.Resource],
        "to": SDO.CreativeWork,
    },
]

predicate_mappings: list[Mapping] = [
    {
        "key": [DCTERMS.created],
        "to": SDO.dateCreated,
    },
    {
        "key": [DCTERMS.modified],
        "to": SDO.dateModified,
    },
    {
        "key": [DCTERMS.issued],
        "to": SDO.dateIssued,
    },
    {
        "key": [DCTERMS.creator],
        "to": SDO.creator,
    },
    {
        "key": [DCTERMS.publisher],
        "to": SDO.publisher,
    },
    {
        "key": [DCTERMS.license],
        "to": SDO.license,
    },
    {
        "key": [DCTERMS.spatial],
        "to": SDO.spatialCoverage,
    },
    {
        "key": [DCTERMS.temporal],
        "to": SDO.temporalCoverage,  # need coverageStartTime & coverageEndTime?
    },
    {
        "key": [DCTERMS.accessRights, DCAT.accessRights],  # dcat:accessRights found in spatial datasets as a typo
        "to": SDO.usageInfo,
    },
    {
        "key": [DCTERMS.language],
        "to": SDO.inLanguage,  # unsure of this one
    },
    # {
    #     "key": [DCTERMS.source, DCAT.accessURL], # unsure if dcterms:source always maps to the same thing
    #     "to": (SDO.distribution, SDO.url), # tuple - bnode chain
    # },
    {
        "key": [DCTERMS.identifier],
        "to": SDO.identifier,
    },
    {
        "key": [DCTERMS.description],
        "to": SDO.description,
    },
    {
        "key": [PROV.agent],
        "to": SDO.agent,
    },
    {
        "key": [DCTERMS.title, RDFS.label],
        "to": SDO.name,
    },
    {
        "key": [DCAT.theme, DCAT.keyword],
        "to": SDO.keywords,
    },
    {
        "key": [DCTERMS.hasPart],
        "to": SDO.hasPart,
    },
    {
        "key": [DCTERMS.isPartOf],
        "to": SDO.isPartOf,
    },
    {
        "key": [REG.status],
        "to": SDO.status,
    },
    # {
    #     "key": [DCTERMS.source, PROV.wasDerivedFrom],
    #     "to": SDO.isBasedOn,
    # },
    # TODO: unmapped predicates
    # dcterms:rights -> sdo:copyrightNotice?
    # indigeneity - currently using dcterms:type
    # dcterms:provenance
    # dcat:hadRole & prov:hadRole
    # dcat:downloadURL
    # dcterms:date
]


class BnodeType(TypedDict):
    predicate: URIRef
    type: URIRef


bnode_types: list[BnodeType] = [
    {
        "predicate": PROV.qualifiedAttribution,
        "type": PROV.Attribution,
    },
    {
        "predicate": PROV.qualifiedDerivation,
        "type": PROV.Derivation,
    },
    {
        "predicate": PROV.qualifiedGeneration,
        "type": PROV.Generation,
    },
    {
        "predicate": DCAT.distribution,
        "type": DCAT.Distribution,
    },
    {
        "predicate": DCAT.qualifiedRelation,
        "type": DCAT.Relationship,
    },
]


def main():
    leftovers = set()

    for file in [f for f in DIRECTORY.glob("**/*.ttl")]:
        g = Graph().parse(file, format="turtle")

        for mapping in type_mappings:
            for t in mapping["key"]:
                for s in g.subjects(RDF.type, t):
                    g.add((s, RDF.type, mapping["to"]))
                    g.remove((s, RDF.type, t))

        for mapping in predicate_mappings:
            for p in mapping["key"]:
                for s, o in g.subject_objects(p):
                    if isinstance(mapping["to"], tuple):  # create bnode chain
                        bnode = BNode()
                        for index, pp in enumerate(mapping["to"]):
                            if index == 0:  # first
                                g.add((s, pp, bnode))
                            elif index < len(mapping["to"]) - 1:  # middle
                                bnode2 = BNode()
                                g.add((bnode, pp, bnode2))
                                bnode = bnode2
                            else:  # last
                                g.add((bnode, pp, o))
                    else:
                        g.add((s, mapping["to"], o))
                    g.remove((s, p, o))

        # add any missing types to bnodes, e.g. prov:qualifiedAttribution [ a prov:Attribution ] etc
        for bnode_type in bnode_types:
            for s, o in g.subject_objects(bnode_type["predicate"]):
                types = g.objects(o, RDF.type)
                if bnode_type["type"] not in types:
                    g.add((o, RDF.type, bnode_type["type"]))

        # special prefixes for vocabs
        cs = g.value(None, RDF.type, SKOS.ConceptScheme)
        if cs is not None:
            g.bind("cs", cs)
            g.bind("", Namespace(str(cs) + "/"))

        # check if changed and update dateModified?

        g.serialize(destination=file, format="longturtle")

        # list any remaining non-SDO, SKOS or GEO predicates that may need to be mapped
        results = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX sdo: <https://schema.org/>
        SELECT DISTINCT ?p
        WHERE {
            ?s ?p ?o .
            FILTER(!STRSTARTS(STR(?p), STR(sdo:)) && !STRSTARTS(STR(?p), STR(skos:)) && !STRSTARTS(STR(?p), STR(geo:)))
        }""")

        for p in results.bindings:
            leftovers.add(str(p["p"]))

    print("Leftover predicates to map:")
    for p in leftovers:
        print(p)


if __name__ == "__main__":
    main()
