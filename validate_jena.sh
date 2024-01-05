#!/usr/bin/bash
mkdir package
/opt/jena/bin/turtle opencs/ontology/core/*/*.ttl > package/core.ttl 2> package/riot.log
/opt/jena/bin/shacl validate --shapes opencs/ontology/shacl_constraints.ttl --data package/core.ttl > package/validation_report.ttl
/opt/jena/bin/sparql --query /app/validation_short_report.rq --data package/validation_report.ttl

