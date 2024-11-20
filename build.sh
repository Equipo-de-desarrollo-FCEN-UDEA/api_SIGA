#!/bin/bash

docker network create siga-fcen
docker compose -f docker/docker-compose.dev.yml up --build

