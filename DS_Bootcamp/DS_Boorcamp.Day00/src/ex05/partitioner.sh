#!/bin/sh 


tail -n +2 "../ex03/hh_positions.csv" | while IFS=, read -r -a line; do
    full_date=$(echo "${line[1]}" | tr -d '"')
    date=$(echo "$full_date" | cut -d'T' -f1)

    filename="${date}.csv"

    if [ ! -f "$filename" ]; then
        head -n 1 "../ex03/hh_positions.csv" > "$filename"
    fi

    echo "${line[*]}" >> "$filename"
done
