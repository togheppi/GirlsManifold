#!/bin/bash
unzip data/erogamescape_sql_output.zip -d data
python -m girls_manifold.scripts.preprocess data/results.html data/results.tsv
