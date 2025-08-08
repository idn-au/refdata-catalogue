from collections import OrderedDict
import os
from pathlib import Path

from dotenv import dotenv_values
from httpx import Client
from prezmanifest.syncer import sync
from prezmanifest.validator import validate
from rich.console import Console
from rich.table import Table


PROJECT_ROOT = Path(__file__).parent
envfile = dotenv_values(".env")
config = {
    "FUSEKI_URL": envfile.get("FUSEKI_URL") or os.environ.get("FUSEKI_URL", ""),
    "FUSEKI_USERNAME": envfile.get("FUSEKI_USERNAME") or os.environ.get("FUSEKI_USERNAME", ""),
    "FUSEKI_PASSWORD": envfile.get("FUSEKI_PASSWORD") or os.environ.get("FUSEKI_PASSWORD", ""),
}


def print_sync_output(status_dict: dict[str, dict], title: str):
    table = Table(title=title, row_styles=["", "dim"])
    table.add_column("File")
    table.add_column("IRI")
    table.add_column("Status")
    table.add_column("Sync")

    for key, value in OrderedDict(sorted(status_dict.items())).items():
        filename = key.split(str(PROJECT_ROOT) + "/")[-1]
        iri = value["main_entity"]
        if value["direction"] == "add-remotely":
            status = "add"
        elif value["direction"] == "upload":
            status = "update"
        else:
            status = ""
        sync = "no" if not value["sync"] else ""

        table.add_row(filename, iri, status, sync)

    console = Console()
    console.print(table)


def sync_large(iri: str, file: Path, client: Client):
    client.post(f"{config["FUSEKI_URL"]}/update", headers={"Content-Type": "application/sparql-update"}, data=f"DROP GRAPH <{iri}>")
    client.post(f"{config["FUSEKI_URL"]}/data", params={"graph": iri}, files={"upload": open(file, "rb")})
    print(f"{str(file).split(str(PROJECT_ROOT) + "/")[-1]} - {iri} uploaded")


def main():
    client = Client(auth=(config["FUSEKI_USERNAME"], config["FUSEKI_PASSWORD"]))

    validate(PROJECT_ROOT / "manifest.ttl")
    print("Manifest is valid")

    pre_status = sync(PROJECT_ROOT / "manifest.ttl", config["FUSEKI_URL"], client, False, False, False, False)
    print_sync_output(pre_status, title="Before sync")

    if all(resource["direction"] == "same" for resource in pre_status.values()):
        print("No sync required")
    else:
        sync(PROJECT_ROOT / "manifest.ttl", config["FUSEKI_URL"], client, True, False, True, False)
        print("Syncable files synced")

        for file in PROJECT_ROOT.glob("vocabs/non-sync/*.ttl"):
            resource = pre_status[str(file)]
            if resource["direction"] != "same":
                sync_large(str(resource["main_entity"]), file, client)
        print("Non-syncable files synced")
                
        
        post_status = sync(PROJECT_ROOT / "manifest.ttl", config["FUSEKI_URL"], client, False, False, False, False)
        print_sync_output(post_status, title="After sync")

        print("Sync complete")


if __name__ == "__main__":
    main()
