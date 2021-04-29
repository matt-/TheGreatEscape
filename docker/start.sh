#!/bin/sh
nohup dockerd --host=unix:///var/run/docker.sock &
timeout 15 sh -c "until docker info; do echo .; sleep 1; done"

cd /docker/nav
docker build --tag simple_service .

docker run --name Navigation simple_service
docker stop Navigation

docker run --name FlightComputer simple_service
docker stop FlightComputer

cd /docker/app
docker build --tag python-docker .
docker run -p 5000:5000 --name CaptainLog -v /var/run/docker.sock:/var/run/docker.sock python-docker
#tail -f /dev/null