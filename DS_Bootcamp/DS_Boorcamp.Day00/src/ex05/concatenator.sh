#!/bin/sh 


head -n 1 $(ls *.csv | head -1) > "result.csv"

files=$(ls *.csv | grep -v "result.csv")

for file in $files; do
    tail -n +2 "$file" >> "result.csv"
done