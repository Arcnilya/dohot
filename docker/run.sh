#!/bin/bash
docker compose down
docker compose build --build-arg TORRC=${1:-default}
docker compose up
