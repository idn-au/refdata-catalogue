from rdflib import Graph

g = Graph().parse("idn-th.ttl")

q = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?b # (COUNT(*) AS ?x)
    WHERE {
        ?c skos:broader ?b .
        MINUS {
        ?b skos:prefLabel ?pl .
        }
    }  
    """

for r in g.query(q):
    print(r)
