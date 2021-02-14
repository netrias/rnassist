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

MODULE="module_subselection_embedding"
OUTPUT_PATH="pipeline/${DATASET}/${MODULE}"

if [ ! -d "${DATA}/${OUTPUT_PATH}" ] 
then
    mkdir "${DATA}/${OUTPUT_PATH}"
fi

cp "${SCRIPT_DIR}/${DATASET}/${MODULE}".json "${DATA}/${OUTPUT_PATH}"/config.json

date
# tried -m 24g successfully. The process took 8.5 hours on Macbook Pro with 2.4 GHz 8-Core Intel Core i9 and 64 GB 2667 MHz DDR4
docker run --rm -m 24g -e config_file="Data/${OUTPUT_PATH}/config.json" -e archive_path="Data/${OUTPUT_PATH}" -e run_num="run3" -v "${DATA}":/assist/Data assist/${MODULE}:0.1.0
date