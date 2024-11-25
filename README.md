# IDN Vocabulary Data


This repository contains part of the data of the Indigenous Data Network (IDN)'s Knowledge Graph which is delivered online via the Prez system as a series of catalogues and reference datasets, such as spatial data collections and vocabularies.

The IDN Prez system is online at:

- https://data.idnau.org

## IDN Catalogues and Datasets

The IDN is producing multiple systems and datasets:

1. [Demonstration Catalogue](https://data.idnau.org/pid/democat) of Australian datasets
    - With varying levels of indigenous relevance to demonstrate several aspects of indigenous data governance, sovereignty and how to even rate the "indigenous-ness" of data in the first place.
2. [Agents Database](https://data.idnau.org/pid/agentsdb)
   - Containing information about Agents - People and Organisations - that have some relation to indigenous data
3. [University of Melbourne’s Indigenous Data Catalogue](https://data.idnau.org/pid/umidcat)
   - this is currently (May, 2023) empty but will fill shortly
4. [Register of vocabularies](https://data.idnau.org/v/vocab)
   - Multiple vocabularies, all assembled and some created, by the IDN that support modelling indigenous data
5. [Indigenous spatial reference data](https://data.idnau.org/s/datasets)
   - Indigenous language, land use, treaty and other areas
   - All from other sources, attributed in the data

Additionally, the IDN will support a catalogue of ANU's indigenous data underdevelopment by ANU’s First National Portfolio that’s not online yet.

This repository contains only some of those system’s data, see next.

## This repository’s content

This repository contains:
- The vocabularies within the IDN’s Register of vocabularies
   - within `data/vocabularies/`
- Background ontologies used to provide labelling for Prez' data
  - within `data/_background/`

  
## Stored elsewhere are:

- Agents Database content
   - some test data is stored here in but the Agents DB is building/storing its own data within it
   - see the [AgentsDB](https://github.com/idn-au/agentsdb-data) data repository
- Indigenous spatial reference data
  - some of these datasets are large so their raw content isn’t directly available
  - see the repo https://github.com/idn-au/spatial-data for a listing of the datasets and instructions on how they are produced

## (Meta)Data Models

The metadata of items in the Demonstration Catalogue and all other catalogues based on IDN work - the UoM IDCat and the ANU’s FNP’s future catalogue - use the [IDN Catalogue Profile](https://w3id.org/idn/def/cp) which is a data cataloguing standard based on [DCAT](https://w3id.org/idn/def/cp.

Agents data in the Agents Database are formulated according to the [Agents Governance Profile](https://w3id.org/idn/def/agp.

## License & Rights

The contents of this repository is licensed under Creative Commons 4.0 International. See the LICENSE file in the repository for details.
## Contact
For technical enquiries:  


**Jamie Feiss  
Data Infrastructure Developer**  
Indigenous Data Network  
University of Melbourne  
[jamie.feiss@unimelb.edu.au](mailto:jamie.feiss@unimelb.edu.au)

For policy:


**Levi Murray  
Strategic Data Manager**  
Indigenous Data Network  
University of Melbourne  
[levi.murray@unimelb.edu.au](mailto:levi.murray@unimelb.edu.au)  

Owner Organisation  
**Indigenous Data Network**  
https://idnau.org


## Prez resources

This listing of the resources in this repository is used by the [Prez System](https://kurrawong.ai/products/prez/) to display the vocabularies correctly.

| Resource             | Location                                                                                                              | Notes                                                        |
|----------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| Catalogue Definition | `catalogue.ttl`                                                                                                       |                                                              |
| Items                | `./vocabs/*.ttl`                                                                                                      | Multiple ttl files                                           |
| Profile Definition   | [Prez Records Profile](https://github.com/RDFLib/prez/blob/main/prez/reference_data/profiles/ogc_records_profile.ttl) | Default Prez profile for Records API                         |
| Context Resources    | `_background/labels.ttl`                                                                                              | A single file containing labels for the catalogue and vocabs |


