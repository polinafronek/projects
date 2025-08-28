#!/bin/sh

{
    echo '"name", "count"'
    tail -n +2 ../ex03/hh_positions.csv | cut -d',' -f3 | grep -v '"-"' | sort | uniq -c | awk '{print $2","$1}'

} > "hh_uniq_positions.csv"