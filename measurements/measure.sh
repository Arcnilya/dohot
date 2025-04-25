#!/bin/bash

resolver=localhost
base_port=1337
queries=100

log() {
    echo "$(date +"%Y-%m-%dT%H:%M:%S"): $1"
}

start_resolver() {
    local port=$1
    local cname=$2
    shift 2
    log "Starting $cname"
    docker run -d -p $port:53/tcp -p $port:53/udp --name "$cname" "$@" dohot-image > /dev/null
    dig @$resolver -p $port kau.se +tries=5 +noall > /dev/null 2>&1
}

stop_resolver() {
    local cname=$1
    log "Stopping $cname"
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
            start_resolver "$port" "$cname" "${docker_env_args[@]}"
            dname="${prot}-${method}-${setting}-$i-$(mktemp -u XXXXXXXX).net"
            log "Sending $dname"
            qtime=$(dig @$resolver -p $port $dname +tries=2 | grep "Query time" | awk '{print $(NF-1)}')
            stop_resolver "$cname"

            if [ "$qtime" ]; then
                echo "$dname,$qtime" >> "$logfile"
                break
            fi
            log "Rebooting $cname"
        done
    done
}

# Kill any leftover containers
docker rm -f $(docker ps -aq --filter name=dohot-) 2>/dev/null

start_time=$(date +%s)

# Run test rounds in parallel
prot="dohot"
run_test_round "$prot" "torrc" "default"    $((base_port + 0)) -e HOPS="3" -e METHOD="torrc" &
run_test_round "$prot" "torrc" "noguard"    $((base_port + 10)) -e HOPS="3" -e METHOD="torrc-noguard" &
run_test_round "$prot" "torrc" "se2any2any" $((base_port + 1)) -e HOPS="3" -e METHOD="torrc" -e ENTRY_NODES="se" &
run_test_round "$prot" "torrc" "se2any2se"  $((base_port + 2)) -e HOPS="3" -e METHOD="torrc" -e ENTRY_NODES="se" -e EXIT_NODES="se" &
run_test_round "$prot" "carml" "twohops"    $((base_port + 3)) -e HOPS="2" -e METHOD="carml" &
run_test_round "$prot" "carml" "threehops"  $((base_port + 4)) -e HOPS="3" -e METHOD="carml" &
run_test_round "$prot" "carml" "se2se"      $((base_port + 5)) -e HOPS="2" -e METHOD="carml" -e ENTRY_NODES="se" -e EXIT_NODES="se" &
run_test_round "$prot" "carml" "se2de"      $((base_port + 6)) -e HOPS="2" -e METHOD="carml" -e ENTRY_NODES="se" -e EXIT_NODES="de" &
run_test_round "$prot" "carml" "se2se2se"   $((base_port + 7)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" -e MIDDLE_NODES="se" -e EXIT_NODES="se" &
run_test_round "$prot" "carml" "se2se2de"   $((base_port + 8)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" -e MIDDLE_NODES="se" -e EXIT_NODES="de" &
run_test_round "$prot" "carml" "se2de2se"   $((base_port + 9)) -e HOPS="3" -e METHOD="carml" -e ENTRY_NODES="se" -e MIDDLE_NODES="de" -e EXIT_NODES="se" &

#prot="dotot"
#run_test_round "$prot" "torrc" "default"   $((base_port + 8)) &
#run_test_round "$prot" "carml" "twohops"   $((base_port + 9)) -e HOPS="2" &
#run_test_round "$prot" "carml" "threehops" $((base_port + 10)) -e HOPS="3" &
#run_test_round "$prot" "carml" "se2se"     $((base_port + 11)) -e ENTRY_NODES="se" -e EXIT_NODES="se" -e HOPS="2" &
#run_test_round "$prot" "carml" "se2de"     $((base_port + 12)) -e ENTRY_NODES="se" -e EXIT_NODES="de" -e HOPS="2" &

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


