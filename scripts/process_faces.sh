#!/bin/bash
python -m girls_manifold.scripts.select_year \
    --input-dir anime_faces/images \
    --output-dir data/2013 \
    --items-path data/chu.jl \
    --games-path data/results.tsv

#python -m girls_manifold.scripts.detect_faces \
#    --input-dir data/selected_images \
#    --output-dir data/detected_faces
