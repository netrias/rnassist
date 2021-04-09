#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo ${SCRIPT_DIR}

DATA="/Volumes/GoogleDrive/Shared drives/NIAAA_ASSIST/Data"

if [[ $1 = "human" || $1 = "mouse" ]]
then
	DATASET=$1
else
	echo "dataset must be either human or mouse"
	exit
fi

MODULE="module_membership_analysis"
CONFIG_PATH="pipeline/${DATASET}/${MODULE}"

if [ ! -d "${DATA}/${CONFIG_PATH}" ]
then
    mkdir "${DATA}/${CONFIG_PATH}"
fi

cp "${SCRIPT_DIR}/${DATASET}/${MODULE}".json "${DATA}/${CONFIG_PATH}/${MODULE}".json

# Takes about 13 minutes to run
date
docker run -m 16g --rm -e config_file="${DATA}/${CONFIG_PATH}/${MODULE}".json -v "${DATA}":"${DATA}" assist/${MODULE}:0.1.0
date