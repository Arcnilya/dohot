#!/bin/bash

ENTRY=""
MIDDLE=""
EXIT=""
EXCLUDE=""
HOPS=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --entry)
            ENTRY="$2"
            shift 2
            ;;
        --middle)
            MIDDLE="$2"
            shift 2
            ;;
        --exit)
            EXIT="$2"
            shift 2
            ;;
        --exclude)
            EXCLUDE="$2"
            shift 2
            ;;
        --hops)
            HOPS="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 --hops <number> --entry <country_code> --middle <country_code> --exit <country_code>"
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done


docker stop dotot-container
docker rm dotot-container
docker build -t dotot-image .
docker run --rm --name dotot-container \
    -e ENTRY_NODES="$ENTRY" \
    -e MIDDLE_NODES="$MIDDLE" \
    -e EXIT_NODES="$EXIT" \
    -e EXCLUDE_NODES="$EXCLUDE" \
    -e HOPS="$HOPS" \
    -p 127.0.0.1:1337:8053/udp \
    -p 127.0.0.1:1337:8053/tcp \
    dotot-image
