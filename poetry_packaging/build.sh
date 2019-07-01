#!/bin/bash

. project.cfg

DOCKER_BUILDKIT=1 \
docker build \
  --tag "$repo:latest" \
  --tag "$repo:$tag" \
  --build-arg PYPI_REPO=$pypirepo \
  .
