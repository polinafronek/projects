#!/bin/sh

if [ -z "$1" ]; then
    echo "Pass the vacancy as an argument"
    exit 1
fi 

vacancy=$1
encoded=$(echo "$vacancy" | jq -sRr @uri)

tmpfile=$(mktemp)

status_code=$(curl -s -w "%{http_code}" -o "$tmpfile" "https://api.hh.ru/vacancies?text=$encoded&per_page=20")

if [ "$status_code" -ne 200 ]; then 
    echo "API ERROR: code $status_code"
    rm -f "$tmpfile"
    exit 1
fi

jq '.'  "$tmpfile" > hh.json
rm "$tmpfile"





