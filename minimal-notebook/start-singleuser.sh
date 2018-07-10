#!/bin/bash

if [ -n "${JUPYTER_PRELOAD_REPOS}" ]; then
    for repo in `echo ${JUPYTER_PRELOAD_REPOS} | tr ',' ' '`; do
        echo "Checking if repository $repo exists locally"
        REPO_DIR=$(basename ${repo})
        if [ -d "${REPO_DIR}" ]; then
            pushd ${REPO_DIR}
            GIT_SSL_NO_VERIFY=true git pull --ff-only
            popd
        else
            GIT_SSL_NO_VERIFY=true git clone ${repo} ${REPO_DIR}
        fi
    done
fi

set -eo pipefail

if [[ "$NOTEBOOK_ARGS $@" != *"--ip="* ]]; then
  NOTEBOOK_ARGS="--ip=0.0.0.0 $NOTEBOOK_ARGS"
fi

NOTEBOOK_ARGS="$NOTEBOOK_ARGS --config=/opt/app-root/configs/jupyter_notebook_config.py"

if [ ! -z "$JUPYTER_ENABLE_LAB" ]; then
  NOTEBOOK_BIN="jupyter labhub"
else
  NOTEBOOK_BIN="jupyterhub-singleuser"
fi

. /opt/app-root/bin/start.sh $NOTEBOOK_BIN $NOTEBOOK_ARGS "$@"
