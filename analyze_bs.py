from pathlib import Path
import argparse
from os import fspath

from pyLCIO.io import LcioReader

inputFileDefault = (
    Path.home()
    / "promotion/data/TEST_IMPROVED/ILD_FCCee_v01/pairs-1_ZHatIP_tpcTimeKeepMC_keep_microcurlers_10MeV_30mrad_ILD_FCCee_v01.slcio"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputFile",
        "-f",
        default=fspath(inputFileDefault),
        type=str,
        help="relative path to the input file",
    )

    args = parser.parse_args()
    inputFile = args.inputFile

    reader = LcioReader.LcioReader(inputFile)

    from IPython import embed; import time; embed(); time.sleep(1)

main()
