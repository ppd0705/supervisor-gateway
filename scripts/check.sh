#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi
export SOURCE_FILES="supervisor_gateway tests"

set -x
set -e

${PREFIX}black --check --diff --target-version=py38 $SOURCE_FILES
${PREFIX}flake8 $SOURCE_FILES
${PREFIX}isort --check --diff --project=supervisor_gateway $SOURCE_FILES
${PREFIX}mypy $SOURCE_FILES
