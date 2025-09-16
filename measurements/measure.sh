#!/bin/bash

resolver=localhost
base_port=1337
queries=10

log() {
    echo "$(date +"%Y-%m-%dT%H:%M:%S"): $1"
}

start_resolver() {
    local prot=$1
    local port=$2
    local cname=$3
    shift 3
    #log "Starting $cname"
    docker run -d -p $port:53/tcp -p $port:53/udp --name "$cname" "$@" $prot-image > /dev/null
    dig @$resolver -p $port kau.se +tries=5 +short +noall > /dev/null 2>&1
}

stop_resolver() {
    local cname=$1
    #log "Stopping $cname"
    docker stop "$cname" > /dev/null
    docker rm "$cname" > /dev/null
}

run_test_round() {
    local prot="$1"
    local method="$2"
    local setting="$3"
    local port="$4"
    local cname="${prot}-${method}-${setting}"
    local logfile="log-${prot}-${method}-${setting}.csv"
    shift 4
    local docker_env_args=("$@")

    echo "query,time" > "$logfile"

    for i in $(seq 0 $((queries - 1))); do
        while :; do
            start_resolver "$prot" "$port" "$cname" "${docker_env_args[@]}"
            dname="${prot}-${method}-${setting}-$i-$(mktemp -u XXXXXXXX).net"
            log "Sending $dname"
            qtime=$(dig @$resolver -p $port $dname +tries=3 | grep "Query time" | awk '{print $(NF-1)}')
            stop_resolver "$cname"

            if [ "$qtime" ]; then
                echo "$dname,$qtime" >> "$logfile"
                break
            fi
            #log "Rebooting $cname"
        done
    done
}

# Kill any leftover containers
docker rm -f $(docker ps -aq --filter name=dohot-) 2>/dev/null
docker rm -f $(docker ps -aq --filter name=dotor-) 2>/dev/null
docker rm -f $(docker ps -aq --filter name=odoh-) 2>/dev/null

start_time=$(date +%s)

# Run test rounds in parallel

## Plot 1: torrc vs stem+carml
run_test_round "dohot" "torrc" "any2any2any" $((base_port + 0)) -e HOPS="3" -e METHOD="torrc" &
run_test_round "dohot" "carml" "any2any2any" $((base_port + 1)) -e HOPS="3" -e METHOD="carml" &
run_test_round "dohot" "torrc" "se2any2any" $((base_port + 2)) -e HOPS="3" -e METHOD="torrc" -e ENTRY_NODES="se" &
run_test_round "dohot" "carml" "se2any2any" $((base_port + 3)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" &
run_test_round "dohot" "torrc" "se2any2se" $((base_port + 4)) -e HOPS="3" -e METHOD="torrc" -e ENTRY_NODES="se" -e EXIT_NODES="se" &
run_test_round "dohot" "carml" "se2any2se" $((base_port + 5)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" -e EXIT_NODES="se" &

## Plot 2: swedish middle
run_test_round "dohot" "carml" "any2se2any" $((base_port + 6)) -e HOPS="3" -e METHOD="carml" -e MIDDLE_NODES="se" &
run_test_round "dohot" "carml" "se2se2any" $((base_port + 7)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" -e MIDDLE_NODES="se" &
run_test_round "dohot" "carml" "any2se2se" $((base_port + 8)) -e HOPS="3" -e METHOD="carml" -e MIDDLE_NODES="se" -e EXIT_NODES="se" &
run_test_round "dohot" "carml" "se2se2se" $((base_port + 9)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" -e MIDDLE_NODES="se" -e EXIT_NODES="se" &

#wait

## Plot 3: only entry and exit
run_test_round "dohot" "carml" "any2any" $((base_port + 10)) -e HOPS="2" -e METHOD="carml" &
run_test_round "dohot" "carml" "se2any" $((base_port + 11)) -e HOPS="2" -e METHOD="carml" -e ENTRY_NODES="se" &
run_test_round "dohot" "carml" "any2se" $((base_port + 12)) -e HOPS="2" -e METHOD="carml" -e EXIT_NODES="se" &
run_test_round "dohot" "carml" "se2se" $((base_port + 13)) -e HOPS="2" -e METHOD="carml" -e ENTRY_NODES="se" -e EXIT_NODES="se" &

## Plot 4: dohot (old vs new) vs odoh
run_test_round "odoh" "default" "default" $((base_port + 14)) &

## Plot 5 or Misc
### Worst
run_test_round "dohot" "carml" "au2se2au" $((base_port + 15)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="au" -e MIDDLE_NODES="se" -e EXIT_NODES="au" &
### Same continent
run_test_round "dohot" "carml" "se2de" $((base_port + 16)) -e HOPS="2" -e METHOD="carml" -e ENTRY_NODES="se" -e EXIT_NODES="de" &
### Different continent
run_test_round "dohot" "carml" "se2us" $((base_port + 17)) -e HOPS="2" -e METHOD="carml" -e ENTRY_NODES="se" -e EXIT_NODES="us" &

## Plot 6: DoTor
run_test_round "dotor" "torrc" "any2any2any" $((base_port + 18)) -e HOPS="3" -e METHOD="torrc" &
run_test_round "dotor" "carml" "any2any2any" $((base_port + 19)) -e HOPS="3" -e METHOD="carml" &
run_test_round "dotor" "carml" "se2se2se" $((base_port + 20)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" -e MIDDLE_NODES="se" -e EXIT_NODES="se" &
run_test_round "dotor" "carml" "se2se" $((base_port + 21)) -e HOPS="2" -e METHOD="carml" -e ENTRY_NODES="se" -e EXIT_NODES="se" &

wait

diff=$(($(date +%s) - start_time))
hours=$((diff / 3600))
minutes=$(((diff % 3600) / 60))
seconds=$((diff % 60))
echo "Measurement took: ${hours}h ${minutes}m ${seconds}s"

# Merge logs
log "Merging logs into log.csv..."
echo "query,time" > log.csv
cat log-*.csv | grep -v "query,time" >> log.csv
rm log-*.csv
log "Done. Final log is in log.csv"
