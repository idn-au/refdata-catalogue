import os
from pathlib import Path
import argparse
import httpx
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS, DCAT

TRIPLESTORE_URL = os.environ.get("TRIPLESTORE_URL", "")
TRIPLESTORE_USERNAME = os.environ.get("TRIPLESTORE_USERNAME", "")
TRIPLESTORE_PASSWORD = os.environ.get("TRIPLESTORE_PASSWORD", "")
TIMEOUT = 30.0

BACKGROUND_GRAPH_IRI = "https://vocab-background-data"


def upload_background():
    """Upload .ttl files from _background/
    Drops the Graph specified by BACKGROUND_GRAPH_IRI
    and then uploads all the .ttl files from _background a graph of the same name.
    """
    print("Uploading background data...")
    # drop named graph
    sparql_update_query(f"DROP GRAPH <{BACKGROUND_GRAPH_IRI}>")
    # upload everything in _background/
    project_root = Path(__file__).parent
    for file in project_root.glob(f"{project_root}/_background/*.ttl"):
        upload_named_graph(file, BACKGROUND_GRAPH_IRI, False)
    print("Upload complete")


def upload_vocabs():
    """Uploads vocab files into their own named graphs."""
    print("Uploading vocabularies...")
    # upload vocabs in data/vocabularies/
    project_root = Path(__file__).parent
    for file in project_root.glob(f"{project_root}/vocabs/*.ttl"):
        iri = find_named_graph(file, SKOS.ConceptScheme)
        upload_named_graph(file, iri)
    print("Upload complete")


# returns named graph IRI from class
def find_named_graph(file: Path, object_class: URIRef) -> str:
    """Finds the IRI of the object from a file based on a specified class."""
    g = Graph().parse(file, format="ttl")
    for s in g.subjects(RDF.type, object_class):
        return s


def upload_named_graph(file: Path, iri: str, drop_graph: bool = True):
    """Uploads a named graph from an IRI to the triplestore."""
    # drop named graph
    if drop_graph:
        sparql_update_query(f"DROP GRAPH <{iri}>")
    # upload turtle to the named graph
    sparql_upload_file(file, iri)


# POST request to triplestore with credentials
# need one function for turtle data, one for SPARQL update queries
def sparql_update_query(query: str):
    """Does a SPARQL update request to the triplestore."""
    r = httpx.post(
        url=f"{TRIPLESTORE_URL}/update",
        auth=(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD),
        timeout=TIMEOUT,
        data=query,
        headers={"Content-Type": "application/sparql-update"},
    )


def sparql_upload_file(file: Path, named_graph: str):
    """Uploads a turtle file in a named graph to the triplestore."""
    with open(file, "rb") as f:
        content = f.read()
    r = httpx.post(
        url=f"{TRIPLESTORE_URL}/data",
        auth=(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD),
        timeout=TIMEOUT,
        params={"graph": named_graph},
        content=content,
        headers={"Content-Type": "text/turtle"},
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--background",
        help="Update the background data",
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()
    if args.background:
        upload_background()
    else:
        upload_vocabs()


if __name__ == "__main__":
    main()
