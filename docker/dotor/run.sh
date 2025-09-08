#!/bin/bash

ENTRY=""
MIDDLE=""
EXIT=""
EXCLUDE=""
HOPS=""
METHOD=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --hops)
            HOPS="$2"
            shift 2
            ;;
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
	--method)
	    METHOD="$2"
	    shift 2
	    ;;
        --exclude)
            EXCLUDE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 --hops <number> --entry <country_code> --middle <country_code> --exit <country_code> --method <torrc/carml>"
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
    -e MIDDLE_NODES="$MIDDLE" \
    -e EXIT_NODES="$EXIT" \
    -e EXCLUDE_NODES="$EXCLUDE" \
    -e HOPS="$HOPS" \
    -e METHOD="$METHOD" \
    -p 127.0.0.1:1337:53/udp \
    -p 127.0.0.1:1337:53/tcp \
    dotor-image
