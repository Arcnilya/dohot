#!/bin/bash

ENTRY=""
EXIT=""
EXCLUDE=""
HOPS=3

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --entry)
            ENTRY="$2"
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
            echo "Usage: $0 --entry <country_code> --exit <country_code> --exclude <country_code> --hops <number>"
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

docker stop dotor-container
docker rm dotor-container
docker build -t dotor-image .
docker run --rm --name dotor-container \
    -e ENTRY_NODES="$ENTRY" \
    -e EXIT_NODES="$EXIT" \
    -e EXCLUDE_NODES="$EXCLUDE" \
    -e HOPS="$HOPS" \
    -p 127.0.0.1:1337:1337/udp \
    -p 127.0.0.1:1337:1337/tcp \
    dotor-image
