#!/bin/bash

parse () {
   echo "$1" | sed 's/,/},{/g; s/{/{/; s/}/}/'
} 

TORRC_PATH="/etc/tor/torrc"
if [ "$HOPS" = "3" ]; then
    [[ -n "$ENTRY_NODES" ]] && echo "EntryNodes {$(parse $ENTRY_NODES)}" >> "$TORRC_PATH"
    [[ -n "$EXIT_NODES" ]] && echo "ExitNodes {$(parse $EXIT_NODES)}" >> "$TORRC_PATH"
    [[ -n "$EXCLUDE_NODES" ]] && echo "ExcludeNodes {$(parse $EXCLUDE_NODES)}" >> "$TORRC_PATH"
    [[ -n "$EXCLUDE_NODES" ]] && echo "StrictNodes 1" >> "$TORRC_PATH"
    cat $TORRC_PATH
else
    echo "UseEntryGuards 0" >> "$TORRC_PATH"
fi
service tor restart

if [ "$HOPS" = "2" ]; then
    echo "Creating a two-hop circuit"
    fp1=$(python3 relays.py --cc ${ENTRY_NODES:-any} --role entry)
    echo "Found $fp1"
    fp2=$(python3 relays.py --cc ${EXIT_NODES:-any} --role exit)
    echo "Found $fp2"
    while true; do
        out=$(carml circ -b "$fp1,$fp2")
        echo $out
        id=$(echo $out | grep -o "Circuit ID [0-9]\+" | awk '{print $NF}')
        if [ -n "$id" ]; then
            echo "Circuit $id successfully built"
            carml stream --attach $id &
            echo "Attaching all new streams to circuit: $id"
            break
        fi
    done
fi

dnscrypt-proxy -check
#dnscrypt-proxy -list
dnscrypt-proxy

