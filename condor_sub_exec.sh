#!/bin/bash
source /afs/desy.de/user/k/keyworth/small_code/setup/setup6.sh
n=90
printf '*%.0s' $(seq 1 $n); printf '\n'
echo ddsim "$@"
printf '*%.0s' $(seq 1 $n); printf '\n'
echo ${K4GEO}
printf '*%.0s' $(seq 1 $n); printf '\n'
ddsim "$@"
