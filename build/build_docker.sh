#!/usr/bin/env bash

echo "Building aladdin-demo docker image (~30 seconds)"

BUILD_PATH="$(cd "$(dirname "$0")"; pwd)"
PROJ_ROOT="$(cd "$BUILD_PATH/.." ; pwd)"
PRINT_ONLY="${PRINT_ONLY:-false}"
HASH="${HASH:-local}"
ALL="${ALL:-false}"

print_only_cmd_wrapper() {
    typeset cmd="$1"
    echo "$cmd"
    if ! $PRINT_ONLY; then
        ${cmd}
    fi
}

docker_build() {
    typeset name="$1" dockerfile="$2" context="$3"
    TAG="$name:${HASH}"
    build_cmd="docker build -t $TAG -f $dockerfile $context"
    print_only_cmd_wrapper "$build_cmd"
}
cd "$PROJ_ROOT"

docker_build "aladdin-demo" "docker/aladdin-demo.Dockerfile" "."

#aws login because we are pulling from ecr for base image
$(aws --profile sandbox ecr get-login)
docker_build "aladdin-demo-commands" "docker/aladdin-demo-commands.Dockerfile" "."