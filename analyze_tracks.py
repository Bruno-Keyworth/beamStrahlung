from os import fspath
from pathlib import Path

from podio import root_io

input_file_path = (
    Path.home()
    / "promotion/code/ILDConfig/StandardConfig/production/data/muon_tracking_test_if1_REC.edm4hep.root"
)


def main():
    f = root_io.Reader(fspath(input_file_path))
    e = f.get("events")[0]
    t = e.get("SiTracksCT")[0]
    n_tracker_hits_si_track = t.trackerHits_size()
    print(f"{n_tracker_hits_si_track} hits were found for the SiTracksCT")


if __name__ == "__main__":
    main()
