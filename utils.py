import re

from rdflib import Graph, Node

def serialize_longtrig(g: Graph, graph_iri: Node) -> str:
    """Serializes TriG with longturtle format"""
    ttl_str = g.serialize(format="longturtle")
    return re.sub(r'(PREFIX.+\n\n)', rf'\1<{str(graph_iri)}> {{\n', ttl_str) + "\n}"
