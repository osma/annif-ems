#!/usr/bin/env python

import pymarc
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, SKOS
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

# Load the MARCXML file
records = pymarc.parse_xml_to_array(infile)

# Initialize RDF graph
g = Graph()

# Iterate through each record in the MARCXML file
for record in records:
    # Create a new SKOS concept for each record
    concept_uri = URIRef(record['024'].value())

    g.add((concept_uri, RDF.type, SKOS.Concept))

    # Process datafields
    for field in record.get_fields():
        if field.tag in {'148', '150', '151'}:
            pref_label = field.get_subfields('a')[0]
            g.add((concept_uri, SKOS.prefLabel, Literal(pref_label, lang='et')))
        elif field.tag in {'448', '450', '451'}:
            alt_label = field.get_subfields('a')[0]
            if field.indicators[1] == '9':
                g.add((concept_uri, SKOS.altLabel, Literal(alt_label, lang='en')))
            else:
                g.add((concept_uri, SKOS.altLabel, Literal(alt_label, lang='et')))
        elif field.tag in {'548', '550', '551'}:
            for subfield in field.get_subfields('0'):
                related_concept_uri = URIRef(subfield)
                if 'w' in field and field['w'] == 'g':
                    g.add((concept_uri, SKOS.broader, related_concept_uri))
                elif 'w' in field and field['w'] == 'h':
                    g.add((concept_uri, SKOS.narrower, related_concept_uri))
                else:
                    g.add((concept_uri, SKOS.related, related_concept_uri))

# Print the turtle serialization of the RDF graph
g.serialize(format='turtle', destination=outfile)
