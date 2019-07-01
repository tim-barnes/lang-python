#! /bin/bash

. project.cfg

usage='''
Usage:
  ./format.sh [--check]

Arguments:
  --check   Runs formatter in read-only mode
'''

if [[ $# == 0 ]]; then
  args=''
elif [[ $# == 1 ]] && [[ "$1" == '--check' ]]; then
  args='--check .'
else
  echo "$usage"
  exit 1
fi

docker run --rm \
  --name="$name-formatter" \
  --mount type=bind,source="$(pwd -P)/src",destination=/black \
  registry.gitlab.com/tracr/ci-runner-images/python-black:v1.0 \
  $args

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
