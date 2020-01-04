#!/bin/bash

OUTPUT2="$(ps -C python | wc -l)"

if [[ "$OUTPUT2" ==  *"1"* ]]; then
    python amson.py
fi

