import re
from pathlib import Path

from rdflib import Dataset, Graph
from rdflib.namespace import DCAT, GEO, RDF, RDFS

from utils import serialize_longtrig

DIRECTORY = Path(__file__).parent / "datasets"
FILE_SIZE_LIMIT = 80  # MiB


def split_nq_to_trig():
    """Splits the dataset & feature collection metadata into a turtle file and the features to a trig file from a nquads file"""
    for file in [f for f in DIRECTORY.glob("raw/**/*.nq")]:
        print(f"Parsing {file}")
        g = Dataset(default_union=True).parse(file, format="application/n-quads")

        dataset = g.value(None, RDF.type, DCAT.Dataset)
        print(f"Dataset: {dataset}")

        metadata_query = f"""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT {{
            ?d ?p ?o .
            ?o ?p2 ?o2 .
            ?o2 ?p3 ?o3 .
            ?fc ?fp ?fo .
            ?fo ?fp2 ?fo2 .
            ?fo2 ?fp3 ?fo3 .
        }}
        WHERE {{
            BIND(<{str(dataset)}> AS ?d)
            ?d ?p ?o ;
                rdfs:member ?fc .

            OPTIONAL {{
                ?o ?p2 ?o2 .
                FILTER (isBLANK(?o))

                OPTIONAL {{
                    ?o2 ?p3 ?o3 .
                    FILTER (isBLANK(?o2))
                }}
            }}

            ?fc a geo:FeatureCollection ;
                ?fp ?fo .

            FILTER (?fp != rdfs:member)

            OPTIONAL {{
                ?fo ?fp2 ?fo2 .
                FILTER (isBLANK(?fo))

                OPTIONAL {{
                    ?fo2 ?fp3 ?fo3 .
                    FILTER (isBLANK(?fo2))
                }}
            }}
        }}"""

        results = g.query(metadata_query)

        results.graph.serialize(destination=DIRECTORY / "metadata" / f"{file.stem}-metadata.ttl", format="longturtle")

        features_query = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT {{
            ?fc rdfs:member ?f .
            ?f ?p ?o .
            ?o ?p2 ?o2 .
            ?o2 ?p3 ?o3 .
        }}
        WHERE {{
            BIND (<{str(dataset)}> AS ?d)
            ?d rdfs:member ?fc .
            ?fc rdfs:member ?f .
            ?f ?p ?o .

            OPTIONAL {{
                ?o ?p2 ?o2 .
                FILTER (isBLANK(?o))

                OPTIONAL {{
                    ?o2 ?p3 ?o3 .
                    FILTER (isBLANK(?o2))
                }}
            }}
        }}"""

        results2 = g.query(features_query)

        trig_str = serialize_longtrig(results2.graph, dataset)

        with open(DIRECTORY / "temp-features" / f"{file.stem}.trig", "w") as f:
            f.write(trig_str)


def split_fcs():
    """
    Splits the features in a trig file into separate files by feature collection

    If the file exceeds the file size limit, split into separate parts
    """
    for file in DIRECTORY.glob("temp-features/*.trig"):
        d = Dataset().parse(file, format="application/trig")
        print(f"Parsed {file.name}")

        g = list(d.graphs())[0]

        fcs = g.subjects(RDFS.member, None, unique=True)

        for fc in fcs:
            print(fc)

            features_query = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            CONSTRUCT {{
                ?fc rdfs:member ?f .
                ?f ?p ?o .
                ?o ?p2 ?o2 .
                ?o2 ?p3 ?o3 .
            }}
            WHERE {{
                BIND (<{str(fc)}> AS ?fc)
                ?fc rdfs:member ?f .
                ?f ?p ?o .

                OPTIONAL {{
                    ?o ?p2 ?o2 .
                    FILTER (isBLANK(?o))

                    OPTIONAL {{
                        ?o2 ?p3 ?o3 .
                        FILTER (isBLANK(?o2))
                    }}
                }}
            }}"""

            results = g.query(features_query)
            turtle_str = results.graph.serialize(format="longturtle")
            size = len(turtle_str.encode("utf-8")) / 1024 / 1024
            print(f"size: {size} MiB")

            if size >= FILE_SIZE_LIMIT:
                print("File too large, splitting...")
                prefixes = re.search(r'^((.+\n)*PREFIX.+)\n\n', turtle_str).groups()[0]

                content = re.split(r'\n\.\n\n', turtle_str, 1)[1]
                content = re.sub(r'}$', "", content)
                chunk_size = [0]
                last_space = [0]
                index = 0
                lines = content.splitlines()

                for line_number, line in enumerate(lines):
                    chunk_size[index] += len((line + "\n").encode("utf-8"))
                    if line == "":
                        last_space[index] = line_number
                    if (chunk_size[index] / 1024 / 1024) >= FILE_SIZE_LIMIT:
                        chunk_size.append(0)
                        last_space.append(0)
                        index += 1

                for index, line_no in enumerate(last_space):
                    if index == 0:
                        chunk_str = "\n".join(lines[:line_no])
                    elif index == len(last_space) - 1:
                        chunk_str = "\n".join(lines[last_space[index - 1]:])
                    else:
                        chunk_str = "\n".join(lines[last_space[index - 1]:line_no])

                    gg = Graph().parse(data=prefixes + "\n\n" + chunk_str, format="turtle")

                    features = gg.subjects(RDF.type, GEO.Feature)

                    fc_str = f"""<https://data.idnau.org/pid/agil/point-locations>
                        rdfs:member
                            {" ,\n".join([f"<{str(f)}>" for f in features]) + " ;"}
                    ."""
                    gg.parse(data=prefixes + "\n\n" + fc_str, format="turtle")

                    trig_str = serialize_longtrig(gg, g.identifier)

                    with open(DIRECTORY / "features" / f"{file.stem}-{str(fc).split('/')[-1]}-part{index + 1}.trig",
                              "w") as f:
                        f.write(trig_str)
            else:
                trig_str = serialize_longtrig(results.graph, g.identifier)

                with open(DIRECTORY / "features" / f"{file.stem}-{str(fc).split('/')[-1]}.trig", "w") as f:
                    f.write(trig_str)


if __name__ == "__main__":
    # split_nq_to_trig()
    split_fcs()
