from pyshacl import validate
from rdflib import Graph

def validate_shacl(g: Graph):

  shacl_file = '''\
  @prefix ex: <http://datashapes.org/shasf/tests/expression/advanced.test.shacl#> .
  @prefix exOnt: <http://datashapes.org/shasf/tests/expression/advanced.test.ont#> .
  @prefix exData: <http://datashapes.org/shasf/tests/expression/advanced.test.data#> .
  @prefix owl: <http://www.w3.org/2002/07/owl#> .
  @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
  @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
  @prefix sh: <http://www.w3.org/ns/shacl#> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
  @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
  <http://datashapes.org/shasf/tests/expression/advanced.test.shacl>
    rdf:type owl:Ontology ;
    rdfs:label "Test of advanced features" ;
  .

  ex:SinglePrefLabelPerLanguageRule
    a sh:NodeShape ;
    sh:targetClass skos:Concept  ;
      sh:message "Concept needs to have at most one skos:prefLabel per language" ;
    sh:property [
      sh:path skos:prefLabel ;
      sh:uniqueLang true ;
    ] .

  ex:SingleDefinitionPerLanguageRule
    a sh:NodeShape ;
    sh:targetClass skos:Concept  ;
      sh:message "Concept needs to have at most one skos:definition per language" ;
    sh:property [
      sh:path skos:definition ;
      sh:uniqueLang true ;
    ] .

  ex:NonRootsHaveSingleBroaderRule
      a sh:NodeShape ;
    sh:targetClass skos:Concept  ;
      sh:message "Concepts other than Computer Science need broader concept" ;
      sh:or (
      [
        sh:property [
          sh:path skos:broader ;
          sh:minCount 1 ;
        ]
      ]
      [
        sh:property [
              sh:path skos:prefLabel ;
              sh:pattern "^Computer science$" ;
            ] ;
      ]
    ) .

  ex:NoCyclesRule
    a sh:NodeShape ;
    sh:targetClass skos:Concept  ;
      sh:message "Path longer than 9 detected" ;
    sh:property [
      sh:path  (skos:broader skos:broader skos:broader skos:broader skos:broader skos:broader skos:broader skos:broader skos:broader) ;
      sh:maxCount 0 ;
    ] .

  '''
  
  report = validate(g,
      shacl_graph=shacl_file,
      ont_graph=None,
      inference=None,
      abort_on_first=False,
      allow_infos=False,
      allow_warnings=False,
      meta_shacl=False,
      advanced=False,
      js=False,
      debug=False)
  conforms, results_graph, results_text = report
  if not conforms:
    print(results_text)
    exit(1)
   else:
    print('Validated! No issues found!')
