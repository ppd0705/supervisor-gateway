#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi
export SOURCE_FILES="supervisor_gateway tests"

set -x

${PREFIX}autoflake --in-place --recursive $SOURCE_FILES
${PREFIX}isort --sl --project=supervisor_gateway $SOURCE_FILES
${PREFIX}black $SOURCE_FILES
#${PREFIX}vulture $SOURCE_FILES --min-confidence 70