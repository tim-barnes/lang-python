#! /bin/bash

. project.cfg

# Are we running inside a terminal or on CI?
if [ -t 1 ]; then
    INTERACTIVE_FLAG="-it"
else
    INTERACTIVE_FLAG=""
fi
    
DOCKER_BUILDKIT=1 \
docker build \
  --target=test \
  --tag="$repo:tests" \
  . || exit 1

docker run ${INTERACTIVE_FLAG} --rm \
  --mount type=bind,source="$(pwd -P)/src",destination=/app \
  --name="unit-test-$name" \
  "$repo:tests" \
  $@

# Some "docker run" options for quick reference:
#  --env VARIABLE=value
#  --publish, -p HOST_PORT:CONTAINER_PORT
#  --volume=[HOST_PATH|NAMED_VOLUME]:DEST_PATH[:ro]
#  --mount type=bind,source=HOST_PATH,destination=DEST_PATH[,readonly]
#  --mount type=volume[,source=NAMED_VOLUME],destination=DEST_PATH[,readonly]
#  --mount type=tmpfs,destination=DEST_PATH
#
# NB:
#  - Volume will create DEST_PATH if it doesn't already exist
#  - Mount and Volume require absolute paths, and cannot deal with symlinks
