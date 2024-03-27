import csv
from datetime import datetime

import rdflib
from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import GEO, RDF, RDFS, SDO, SKOS, XSD

cs = URIRef("https://data.idnau.org/pid/austlang")
AL = Namespace("https://data.idnau.org/pid/austlang/")

ST = {
    "ACT": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/8"),
    "NSW": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/1"),
    "NT": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/7"),
    "OT": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/9"),
    "TSI": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/3"),
    "OA": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/Z"),
    "QLD": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/3"),
    "SA": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/4"),
    "TAS": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/6"),
    "VIC": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/2"),
    "WA": URIRef("https://linked.data.gov.au/dataset/asgsed3/STE/5"),
}


dt = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <https://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    <https://data.idnau.org/pid/austlang/AustLangCode>
        a rdfs:DataType ;
        rdfs:label "AustLang Code" ;
        rdfs:comment "Codes assigned to Australian Aboriginal languages within the AIATSIS AustLang dataset" ;
        schema:citation "https://collection.aiatsis.gov.au/austlang"^^xsd:anyURI ;
    .
"""

g1 = Graph()

with open("../vocabs/sources/austlang_dataset.csv") as f:
    data = csv.reader(f)
    data.__next__()
    for row in data:
        c = AL[row[0]]
        g1.add((c, RDF.type, SKOS.Concept))
        g1.add((c, SKOS.prefLabel, Literal(row[1].strip(), lang="aus")))
        g1.add((c, SKOS.definition, Literal(row[3], lang="en")))
        g1.add((c, SKOS.notation, Literal(row[0], datatype=AL.AustLangCode)))
        for word in row[2].split(","):
            g1.add((c, SKOS.altLabel, Literal(word.strip())))
        if row[7] is not None and row[7] != "":
            for st in row[7].split(","):
                g1.add((c, GEO.sfWithin, ST[st]))
        g1.add((c, SDO.citation, Literal(row[8], datatype=XSD.anyURI)))

        g1.add((c, SKOS.inScheme, cs))
        g1.add((c, SKOS.topConceptOf, cs))
        g1.add((cs, SKOS.hasTopConcept, c))
        g1.add((c, RDFS.isDefinedBy, cs))
        g1.add((
            c,
            SKOS.historyNote,
            Literal(f"Extracted from the AustLang datasets on data.gov.au, {datetime.now().strftime('%Y-%m-%d')}")
        ))

austlang_cs = """
    PREFIX : <https://data.idnau.org/pid/austlang/>
    PREFIX cs: <https://data.idnau.org/pid/austlang>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX dataroles: <https://linked.data.gov.au/def/data-roles/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX reg: <http://purl.org/linked-data/registry#>
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    cs:
        a skos:ConceptScheme ;
        reg:status <https://linked.data.gov.au/def/reg-statuses/stable> ;
        owl:versionIRI :0.1 ;
        skos:definition "AustLang provides information about Aboriginal and Torres Strait Islander languages which has been assembled from a number of referenced sources"@en ;
        skos:historyNote "Extracted from the AustLang datasets on data.gov.au, DDD" ;
        skos:prefLabel "AustLang"@en ;
        schema:creator <https://linked.data.gov.au/org/aiatsis> ;
        schema:contributor <https://linked.data.gov.au/org/idn> ;
        schema:dateCreated "2024-03-27"^^xsd:date ;
        schema:dateModified "2024-03-27"^^xsd:date ;
        dcat:keyword
            "Indigenous languages" ,
            "Aboriginal" ;
        schema:publisher <https://linked.data.gov.au/org/idn> ;
        schema:version "0.1" ;
        schema:citation "https://collection.aiatsis.gov.au/austlang"^^xsd:anyURI ;
    .
        
    <https://linked.data.gov.au/org/aiatsis>
        a schema:Organization ;
        schema:name "Australian Institute of Aboriginal and Torres Strait Islander Studies" ;
        schema:url "https://aiatsis.gov.au"^^xsd:anyURI ;
    .

    <https://linked.data.gov.au/org/idn>
        a schema:Organization ;
        schema:name "Indigenous Data Network" ;
        schema:url "https://www.idnau.org"^^xsd:anyURI ;
    .
    """.replace("DDD", datetime.now().strftime('%Y-%m-%d'))

g1.parse(data=austlang_cs, format="turtle")
g1.parse(data=dt, format="turtle")
g1.serialize(destination="../vocabs/austlang.ttl", format="longturtle")

austlang_d = """
    PREFIX : <https://data.idnau.org/pid/austlang/>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    PREFIX geofab: <https://linked.data.gov.au/def/geofabric#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <https://schema.org/>
    PREFIX spacecat: <https://data.idnau.org/pid/spacecat/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    <https://data.idnau.org/pid/spacecat>
        dcterms:hasPart <https://data.idnau.org/pid/austlang> ;
    .
    
    <https://data.idnau.org/pid/austlang>
        a dcat:Dataset ;
        schema:description "AustLang provides information about Aboriginal and Torres Strait Islander languages which has been assembled from a number of referenced sources" ;
        geo:hasBoundingBox [
            a geo:Geometry ;
            geo:asWKT "POLYGON ((96.0 -45.0, 168.0 -45.0, 168.0 -9.0, 96.0 -9.0, 96.0 -45.0))"^^geo:wktLiteral ;
        ] ;
        rdfs:member :austlang-locations ;
        schema:creator <https://linked.data.gov.au/org/aiatsis> ;
        schema:contributor <https://linked.data.gov.au/org/idn> ;
        schema:dateCreated "2024-03-27"^^xsd:date ;
        schema:dateModified "2024-03-27"^^xsd:date ;
        schema:citation "https://collection.aiatsis.gov.au/austlang"^^xsd:anyURI ;
        schema:name "AustLang" ;
    .
    
    :point-locations
        a geo:FeatureCollection ;
        schema:description "All AustLang language locations as points"@en ;
        schema:name "AustLang point locations"@en ;
        geo:hasBoundingBox [
            a geo:Geometry ;
            geo:asWKT "POLYGON ((96.0 -45.0, 168.0 -45.0, 168.0 -9.0, 96.0 -9.0, 96.0 -45.0))"^^geo:wktLiteral ;
        ] ;
    .

    <https://linked.data.gov.au/org/aiatsis>
        a schema:Organization ;
        schema:name "Australian Institute of Aboriginal and Torres Strait Islander Studies" ;
        schema:url "https://aiatsis.gov.au"^^xsd:anyURI ;
    .

    <https://linked.data.gov.au/org/idn>
        a schema:Organization ;
        schema:name "Indigenous Data Network" ;
        schema:url "https://www.idnau.org"^^xsd:anyURI ;
    .
    """.replace("DDD", datetime.now().strftime('%Y-%m-%d'))

g2 = Graph()

g1 = Graph()

with open("../vocabs/sources/austlang_dataset.csv") as f:
    data = csv.reader(f)
    data.__next__()
    for row in data:
        c = AL[row[0]]
        g2.add((c, RDF.type, GEO.Feature))
        g2.add((c, SDO.name, Literal(row[1].strip(), lang="aus")))
        g2.add((c, SDO.description, Literal(row[3], lang="en")))
        g2.add((c, SDO.identifier, Literal(row[0], datatype=AL.AustLangCode)))
        for word in row[2].split(","):
            g2.add((c, SDO.alternateName, Literal(word.strip())))
        geom = BNode()
        g2.add((c, GEO.hasGeometry, geom))
        if row[5] is not None and row[5] != "":
            g2.add((geom, GEO.asWKT, Literal(f'POINT ({row[6]} {row[5]})', datatype=GEO.asWKT)))
        if row[7] is not None and row[7] != "":
            for st in row[7].split(","):
                g2.add((c, GEO.sfWithin, ST[st]))
        g2.add((c, SDO.citation, Literal(row[8], datatype=XSD.anyURI)))

        g2.add((
            c,
            SKOS.historyNote,
            Literal(f"Extracted from the AustLang datasets on data.gov.au, {datetime.now().strftime('%Y-%m-%d')}")
        ))

        g2.add((URIRef("https://data.idnau.org/pid/austlang/point-locations"), RDFS.member, c))

g2.parse(data=austlang_d, format="turtle")
g2.parse(data=dt, format="turtle")
d = rdflib.Dataset()
for s, p, o in g2.triples((None, None, None)):
    d.add((s, p, o, cs))
d.serialize(destination="austlang.nq", format="nquads")
