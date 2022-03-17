#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi

set -x

${PREFIX}pip install -r requirements_dev.txt
${PREFIX}pip install -r requirements_dev.txt
${PREFIX}pip install -e .