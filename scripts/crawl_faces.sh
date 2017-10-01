#!/bin/bash
cd anime_faces ; scrapy crawl getchu -o ../data/chu.jl -a input_path=../data/results.tsv -a output_path=../data/chu.jl
