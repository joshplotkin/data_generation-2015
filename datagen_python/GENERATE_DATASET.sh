#!/usr/local/bin/bash
echo '' > trans_fact.csv
for i in $(seq 1 $1) ; do python EXECUTE.py >> trans_fact.csv ; done
