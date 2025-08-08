# this script is no longer used
import argparse
import os
from pathlib import Path

import httpx
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS

TRIPLESTORE_URL = os.environ.get("TRIPLESTORE_URL", "")
TRIPLESTORE_USERNAME = os.environ.get("TRIPLESTORE_USERNAME", "")
TRIPLESTORE_PASSWORD = os.environ.get("TRIPLESTORE_PASSWORD", "")
TIMEOUT = 30.0
BACKGROUND_GRAPH_IRI = "https://vocab-background-data"
PROJECT_ROOT = Path(__file__).parent.parent


def upload_background():
    """Upload .ttl files from _background/
    Drops the Graph specified by BACKGROUND_GRAPH_IRI
    and then uploads all the .ttl files from _background a graph of the same name.
    """
    print("Uploading background data...")
    # drop named graph
    sparql_update_query(f"DROP GRAPH <{BACKGROUND_GRAPH_IRI}>")
    # upload everything in _background/
    for file in PROJECT_ROOT.glob("_background/*.ttl"):
        print(f"\t{file.name}")
        upload_named_graph(file, BACKGROUND_GRAPH_IRI, False)
    print("Upload complete")


def upload_vocabs():
    """Uploads vocab files into their own named graphs."""
    existing_vocabs = get_existing_vocabs()
    print("Uploading vocabularies...")
    # upload vocabs in vocabs/
    for file in PROJECT_ROOT.glob("vocabs/*.ttl"):
        iri = find_named_graph(file, SKOS.ConceptScheme)
        drop_graph = iri in existing_vocabs
        if drop_graph:
            existing_vocabs.discard(iri)
        print(f"\t{'~' if drop_graph else '+'} <{iri}> - {file.name}")
        upload_named_graph(file, iri, drop_graph=drop_graph)
    # remove old vocabs
    for iri in existing_vocabs:
        print(f"\t- <{iri}>")
        sparql_update_query(f"DROP GRAPH <{iri}>")
    print("Upload complete")


def get_existing_vocabs() -> set[str]:
    """Does a SPARQL query to get the list of current vocabs in the triplestore"""
    query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?cs
        WHERE {
            GRAPH ?cs {
                ?cs a skos:ConceptScheme .
            }
        }
    """
    r = httpx.post(
        url=f"{TRIPLESTORE_URL}/query",
        auth=(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD),
        timeout=TIMEOUT,
        data=query,
        headers={"Content-Type": "application/sparql-query"},
        verify=False,  # for staging certs
    )
    results: list[dict] = r.json()["results"]["bindings"]
    return {result["cs"]["value"] for result in results}


# returns named graph IRI from class
def find_named_graph(file: Path, object_class: URIRef) -> str:
    """Finds the IRI of the object from a file based on a specified class."""
    g = Graph().parse(file, format="ttl")
    for s in g.subjects(RDF.type, object_class):
        return str(s)


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
        verify=False,  # for staging certs
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
        verify=False,  # for staging certs
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
