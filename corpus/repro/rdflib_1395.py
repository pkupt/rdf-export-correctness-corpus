"""Repro probe: RDFLib issue #1395 - "RDFlib makes invalid Turtle cURIs".

Claim under test: rdflib's Turtle serializer emits prefixed names (cURIs) that
its own parser rejects, i.e. the writer produces invalid Turtle.

Run:  python rdflib_1395.py
Exit 0 always; verdict printed.
"""
import sys
import rdflib
from rdflib import Graph

SRC = """
@prefix ex: <https://example.org/term#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://example.org/entity> ex:anchorOf "This press"^^xsd:string ;
            a <http://dbpedia.org/resource/This_(journal)> .
"""

print("rdflib", rdflib.__version__)

g = Graph()
g.parse(data=SRC, format="turtle")
out = g.serialize(format="turtle")
print("--- serialized output ---")
print(out)
print("--- reparse ---")
g2 = Graph()
try:
    g2.parse(data=out, format="turtle")
    print("REPARSE: OK")
    print("triples: in=%d out=%d" % (len(g), len(g2)))
except Exception as e:
    print("REPARSE: FAILED ->", type(e).__name__)
    print(str(e)[:400])
