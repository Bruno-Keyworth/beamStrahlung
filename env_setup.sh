# echo "source key4hep nightlies stack"
# source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
echo "k4 -r 2025-01-28"
source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2025-01-28

# assert that all k4geo path vars point to the same place
echo "set local k4geo"
export k4geo_DIR="$k4gDir"
export K4GEO="$k4geo_DIR"

