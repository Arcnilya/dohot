#!/bin/bash

resolver=localhost
port=1337
docker rm -f dohot-container 2>/dev/null
echo "query,time" > log.csv

prot="DOHOT"

log() {
    echo "$(date +"%Y-%m-%dT%H:%M:%S"): $1"
}

start_resolver() {
    log "Starting resolver with args: $*"
    docker run -d -p $port:53/tcp -p $port:53/udp --name dohot-container "$@" dohot-image > /dev/null
    dig @$resolver -p $port kau.se +tries=5 +noall # wait for resolver
}

stop_resolver() {
    log "Stopping resolver"
    docker stop dohot-container > /dev/null
    docker rm dohot-container > /dev/null
}

send_query() {
    local dname="$1"
    dig @$resolver -p $port $dname +tries=2 | grep "Query time" | awk '{print $(NF-1)}'
}

run_test_round() {
    local setting="$1"
    shift
    local docker_env_args=("$@")

    for i in $(seq 0 9); do
        while :; do
            start_resolver "${docker_env_args[@]}"
            dname="$prot-$setting-$i-$(mktemp -u XXXXXXXX).net"
            log "Sending query ($dname)"
            qtime=$(send_query "$dname")
            stop_resolver

            if [ "$qtime" ]; then
                echo "$dname,$qtime" >> log.csv
                break
            fi
            log "Rebooting resolver and retrying query"
        done
    done
}

# Run all settings
run_test_round "DEFAULT"
run_test_round "TWOHOPS" -e HOPS="2"
run_test_round "SE2SE" -e ENTRY_NODES="se" -e EXIT_NODES="se" -e HOPS="2"
run_test_round "SE2NL" -e ENTRY_NODES="se" -e EXIT_NODES="nl" -e HOPS="2"
