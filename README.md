# IDN Reference Data Catalogue

This repository contains the reference data - background vocabularies, spatial datasets adn models - part of the data of the Indigenous Data Network (IDN)'s Knowledge Graph. This information is available online at:

- https://data.idnau.org

All the resources in this catalogue are listed in the _Prez resources section_ below. These resources are automatically validated and (re)loaded into the catalogue online using the [Prez Manifest](https://pypi.org/project/prezmanifest/) tool.


## License & Rights

The contents of this repository is licensed under [Creative Commons 4.0 International](https://creativecommons.org/licenses/by/4.0/). See the LICENSE file in the repository for details.


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

| Resource                                                                                                                                            | Role                                                                                                                | Description                                                                          |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Catalogue Definition:<br />[`catalogue.ttl`](catalogue.ttl)                                                                                         | [Catalogue Data](https://prez.dev/ManifestResourceRoles/CatalogueData)                                              | The definition of, and medata for, the container which here is a dcat:Catalog object |
| Resource Data:<br />[`vocabs/*.ttl`](vocabs/*.ttl)                                                                                                  | [Resource Data](https://prez.dev/ManifestResourceRoles/ResourceData)                                                | skos:ConceptScheme objects in RDF (Turtle) files in the vocabs/ folder               |
| Profile Definition:<br />[`ogc_records_profile.ttl`](https://github.com/RDFLib/prez/blob/main/prez/reference_data/profiles/ogc_records_profile.ttl) | [Catalogue & Resource Model](https://prez.dev/ManifestResourceRoles/CatalogueAndResourceModel)                      | The default Prez profile for Records API                                             |
| Labels:<br />[`labels.ttl`](labels.ttl)                                                                                                             | [Complete Catalogue and Resource Labels](https://prez.dev/ManifestResourceRoles/CompleteCatalogueAndResourceLabels) | An RDF file containing all the labels for the container content                      |
