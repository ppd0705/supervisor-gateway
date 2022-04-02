#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi
export SOURCE_FILES="supervisor_gateway tests"

set -x


${PREFIX}autoflake --in-place --recursive --remove-all-unused-imports $SOURCE_FILES
${PREFIX}isort --project=supervisor_gateway $SOURCE_FILES
${PREFIX}black --target-version=py38 $SOURCE_FILES
${PREFIX}flake8 $SOURCE_FILES