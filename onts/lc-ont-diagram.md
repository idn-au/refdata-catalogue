```mermaid
classDiagram
direction LR

%% =========
%% Schemes (instances)
%% =========
class TK_Scheme["ConceptScheme: TK Labels [https://data.idnau.org/pid/vocab/tk-labels"] {
  <<skos:ConceptScheme>>
}
class BC_Scheme["ConceptScheme: BC Labels [https://data.idnau.org/pid/vocab/bc-labels"] {
  <<skos:ConceptScheme>>
}
class Notices_Scheme["ConceptScheme: LC Notices [https://data.idnau.org/pid/vocab/lc-notices"] {
  <<skos:ConceptScheme>>
}

%% =========
%% Core SKOS
%% =========
class Concept {
  <<skos:Concept>>
  skos:prefLabel (langString)
  skos:definition (langString)
  skos:scopeNote (langString)
  skos:notation (string)
  skos:inScheme (IRI)
  sdo:citation (anyURI)
  dcterms:identifier (xsd:token)
}
TK_Scheme "1" o-- "*" Concept : skos:hasTopConcept
BC_Scheme "1" o-- "*" Concept : skos:hasTopConcept
Notices_Scheme "1" o-- "*" Concept : skos:hasTopConcept

Concept "*" --> "*" Concept : skos:broader / skos:narrower
Concept "*" --> "*" Concept : skos:relatedMatch

%% =========
%% Local Contexts ontology classes
%% =========
class TKLabel { <<lcont:TKLabel>> }
class BCLabel { <<lcont:BCLabel>> }
class LCNotice { <<lcont:LCNotice>> }

TKLabel --|> Concept
BCLabel --|> Concept
LCNotice --|> Concept

TKLabel "*" --> "1" TK_Scheme : skos:inScheme
BCLabel "*" --> "1" BC_Scheme : skos:inScheme
LCNotice "*" --> "1" Notices_Scheme : skos:inScheme

%% =========
%% Declared properties in lc-ont
%% =========
class relatedNotice {
  <<lcont:relatedNotice>>
  domain: TKLabel, BCLabel
  range: LCNotice
}
TKLabel "*" --> "*" LCNotice : lcont:relatedNotice
BCLabel "*" --> "*" LCNotice : lcont:relatedNotice

class templateText {
  <<lcont:templateText>>
  domain: TKLabel, BCLabel, LCNotice
  range: rdf:langString
}
TKLabel --> templateText : lcont:templateText
BCLabel --> templateText : lcont:templateText
LCNotice --> templateText : lcont:templateText

%% =========
%% ODRL policy pattern
%% =========
class Policy { <<odrl:Policy>> }
class Permission { <<odrl:Permission>> }
class Prohibition { <<odrl:Prohibition>> }
class Duty { <<odrl:Duty>> }
class Action { <<odrl:Action>> }

TKLabel --|> Policy
BCLabel --|> Policy

Policy "1" o-- "*" Permission : odrl:permission
Policy "1" o-- "*" Prohibition : odrl:prohibition
Permission "1" o-- "*" Duty : odrl:duty
Prohibition "1" o-- "*" Duty : odrl:duty
Permission "*" --> "1" Action : odrl:action
Prohibition "*" --> "1" Action : odrl:action
Duty "*" --> "1" Action : odrl:action

class followProtocol {
  <<lcont:followProtocol>>
  skos:prefLabel "Follow protocol"@en
}
followProtocol --|> Action
```
