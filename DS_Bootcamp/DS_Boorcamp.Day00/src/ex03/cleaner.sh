#!/bin/sh

head -n 1 ../ex02/hh_sorted.csv > "hh_positions.csv"

tail -n +2 "../ex02/hh_sorted.csv" | while IFS=',' read -r id created_at name has_test alternate_url; do
    name=$(echo "$name" | sed 's/^"\(.*\)"$/\1/')

    result=''

    if echo "$name" | grep -iq "Junior"; then
        result="Junior"
    fi

    if echo "$name" | grep -iq "Middle"; then
        if [ -n "$result" ]; then
            result="$result/Middle"
        else
            result="Middle"
        fi
    fi

    if echo "$name" | grep -iq "Senior"; then
        if [ -n "$result" ]; then
            result="$result/Senior"
        else
            result="Senior"
        fi
    fi

    if [ -z "$result" ]; then
        result="-"
    fi

    echo "\"$id\",\"$created_at\",\"$result\",\"$has_test\",\"$alternate_url\"" >> hh_positions.csv
done