# IDN Reference Data Catalogue

This repository contains the reference data - background vocabularies, spatial datasets and models - part of the data of the Indigenous Data Network (IDN)'s Knowledge Graph. This information is available online at:

- https://data.dev.idnau.org

All the resources in this catalogue are listed in the _Prez resources section_ below. These resources are automatically validated and (re)loaded into the catalogue online using the [Prez Manifest](https://pypi.org/project/prezmanifest/) tool.

## Updating resources

When a resource is updated, the `dateModified` date should be updated in the resource and the catalogue as the Prez Manifest tool relies on this to determine when to update data.

If a new resource is added to the catalogue, ensure its IRI is added to `dcterms:hasPart` in `catalogue.ttl`.

Pull requests will trigger validation of the manifest, which is required to pass before merging.

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

Resource | Role | Description
--- | --- | ---
Catalogue Definition:<br />[`catalogue.ttl`](catalogue.ttl) | [Catalogue Data](https://prez.dev/ManifestResourceRoles/CatalogueData) | The definition of, and metadata for, the container which here is a dcat:Catalog object
Syncable Resource Data:<br />[`vocabs/sync/*.ttl`](vocabs/sync/*.ttl) | [Resource Data](https://prez.dev/ManifestResourceRoles/ResourceData) | skos:ConceptScheme objects in RDF (Turtle) files in the vocabs/sync/ folder for syncing
Non-syncable Resource Data:<br />[`vocabs/non-sync/*.ttl`](vocabs/non-sync/*.ttl) | [Resource Data](https://prez.dev/ManifestResourceRoles/ResourceData) | skos:ConceptScheme objects in RDF (Turtle) files in the vocabs/non-sync/ folder, to be synced externally
Draft Resource Data:<br />[`vocabs/drafts/persons-indigenous-status.ttl`](vocabs/drafts/persons-indigenous-status.ttl) | [Resource Data](https://prez.dev/ManifestResourceRoles/ResourceData) | skos:ConceptScheme objects in RDF (Turtle) files in the vocabs/drafts/ folder
Profile Definition:<br />[`ogc_records_profile.ttl`](https://github.com/RDFLib/prez/blob/main/prez/reference_data/profiles/ogc_records_profile.ttl) | [Catalogue & Resource Model](https://prez.dev/ManifestResourceRoles/CatalogueAndResourceModel) | The default Prez profile for Records API
Labels:<br />[`labels.ttl`](labels.ttl) | [Complete Catalogue and Resource Labels](https://prez.dev/ManifestResourceRoles/CompleteCatalogueAndResourceLabels) | An RDF file containing all the labels for the container content