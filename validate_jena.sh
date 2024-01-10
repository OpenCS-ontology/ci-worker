#!/usr/bin/bash
mkdir package
/opt/jena/bin/turtle opencs/ontology/core/*/*.ttl > package/core.ttl 2> package/riot.log
/opt/jena/bin/shacl validate --shapes opencs/ontology/shacl_constraints.ttl --data package/core.ttl > package/validation_report.ttl

table=$(/opt/jena/bin/sparql --query /app/validation_short_report.rq --data package/validation_report.ttl)
echo "$table"

messages=($(echo $table | grep -Eo '^|"([^|])*?"|'))

second=${messages[1]}

if [ $second != '"Success"' ]; then
        exit 1;
fi
