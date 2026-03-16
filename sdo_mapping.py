from pathlib import Path
from typing import TypedDict

from rdflib import Graph, URIRef, BNode, Namespace, Dataset
from rdflib.namespace import DCAT, DCTERMS, SDO, PROV, RDF, RDFS, SKOS, GEO

from utils import serialize_longtrig

REG = Namespace("http://purl.org/linked-data/registry#")

# DIRECTORY = Path(__file__).parent / "vocabs/sync"
# DIRECTORY = Path(__file__).parent / "datasets/metadata"
DIRECTORY = Path(__file__).parent / "datasets/features"
# DIRECTORY = Path(__file__).parent.parent / "isu-catalogue/resources"
# DIRECTORY = Path(__file__).parent.parent / "kp-catalogue/resources"

TRIG = True # for parsing TriG files


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
        "to": SDO.temporalCoverage,
    },
    {
        "key": [PROV.startedAtTime],
        "to": SDO.coverageStartTime,
    },
    {
        "key": [PROV.endedAtTime],
        "to": SDO.coverageEndTime,
    },
    {
        "key": [DCTERMS.accessRights, DCAT.accessRights],  # dcat:accessRights found in NNTT spatial dataset as a typo
        "to": SDO.usageInfo,
    },
    {
        "key": [DCTERMS.language],
        "to": SDO.inLanguage,
    },
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
    {
        "key": [DCTERMS.source],
        "to": SDO.citation,
    },
    {
        "key": [DCTERMS.rights],
        "to": SDO.copyrightNotice,
    },
    {
        "key": [DCAT.distribution],
        "to": SDO.distribution,
    },
    {
        "key": [DCAT.downloadURL],
        "to": SDO.contentUrl,
    },
    # {
    #     "key": [DCAT.hadRole, PROV.hadRole],
    #     "to": SDO.roleCode, # roleCode not in schema.org
    # },

    # TODO: unmapped predicates (generated from script) - non geo, sdo & skos
    # dcat:contactPoint
    # dcat:hadRole
    # dcat:qualifiedRelation
    # dcterms:date - found in yirrakala under rico:hasOrHadLocation
    # dcterms:provenance
    # dcterms:replaces
    # dcterms:type - used for indigeneity
    # owl:versionIRI
    # owl:versionInfo
    # prov:entity
    # prov:hadRole
    # prov:qualifiedAttribution
    # prov:qualifiedDerivation
    # prov:wasAttributedTo
    # prov:wasDerivedFrom
    # rdfs:comment
    # rdfs:isDefinedBy
    # rdfs:member
    # rdfs:seeAlso
    # vcard:country-name
    # vcard:fn
    # vcard:hasAddress
    # vcard:hasEmail
    # vcard:hasTelephone
    # vcard:hasValue
    # vcard:locality
    # vcard:postal-code
    # vcard:street-address
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
    # {
    #     "predicate": DCAT.distribution,
    #     "type": DCAT.Distribution,
    # },
    {
        "predicate": SDO.distribution,
        "type": SDO.DataDownload,
    },
    {
        "predicate": DCAT.qualifiedRelation,
        "type": DCAT.Relationship,
    },
    {
        "predicate": GEO.hasGeometry,
        "type": GEO.Geometry,
    },
    {
        "predicate": GEO.hasBoundingBox,
        "type": GEO.Geometry,
    },
]


def main():
    leftovers = set()

    for file in DIRECTORY.glob(f"**/*.{'trig' if TRIG else 'ttl'}"):
        if TRIG:
            d = Dataset().parse(file, format="application/trig")
            g = list(d.graphs())[0]
        else:
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

        # add any missing types to bnodes, e.g. prov:qualifiedAttribution [ a prov:Attribution ]
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

        if TRIG:
            trig_str = serialize_longtrig(g, g.identifier)

            with open(file, "w") as f:
                f.write(trig_str)
        else:
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
