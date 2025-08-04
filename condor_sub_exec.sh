#!/bin/bash
source ${codeDir}/beamStrahlung/env_setup.sh
n=90
printf '*%.0s' $(seq 1 $n); printf '\n'
echo ddsim "$@"
printf '*%.0s' $(seq 1 $n); printf '\n'
echo ${K4GEO}
printf '*%.0s' $(seq 1 $n); printf '\n'
ddsim "$@"
