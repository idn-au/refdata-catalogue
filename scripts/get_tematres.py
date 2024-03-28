import httpx
from rdflib import Graph

g = Graph(bind_namespaces="rdflib")
print(len(g))
for url in [
    # "https://vocabularyserver.com/apais/xml.php?skosTema=3",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=4",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=5",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=6",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=7",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=8",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=9",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=10",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=11",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=12",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=13",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=14",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=15",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=16",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=17",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=18",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=21",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=22",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=23",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=24",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=25",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=26",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=27",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=28",
    # "https://vocabularyserver.com/apais/xml.php?skosTema=29",
    "https://vocabularyserver.com/apais/xml.php?skosTema=765",
    "https://vocabularyserver.com/apais/xml.php?skosTema=1483",
    "https://vocabularyserver.com/apais/xml.php?skosTema=2178",
    "https://vocabularyserver.com/apais/xml.php?skosTema=2179",
    "https://vocabularyserver.com/apais/xml.php?skosTema=1096"
]:
    r = httpx.get(url)
    print(url)
    if not r.is_success:
        print(str(r.status_code) + ": " + url)
    else:
        try:
            g.parse(data=r.text, format="xml")
        except Exception as e:
            print(e)
        print(len(g))

g.serialize(destination="apais2.ttl", format="longturtle")
