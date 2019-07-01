#!/bin/bash

. project.cfg

DOCKER_BUILDKIT=1 \
docker run "$repo:latest"
