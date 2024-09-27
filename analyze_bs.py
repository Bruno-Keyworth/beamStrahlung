import argparse
from dataclasses import dataclass
from os import fspath
from pathlib import Path
from typing import Dict, Tuple, Union

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

# import awkward as ak
import uproot

inputFileDefault = (
    Path.home()
    / "promotion/data/TEST_IMPROVED/ILD_FCCee_v01/pairs-2_ZHatIP_tpcTimeKeepMC_keep_microcurlers_10MeV_30mrad_ILD_FCCee_v01.emd4hep.root"
)


# Define the dataclass
@dataclass
class Collection:
    branch_name: str
    plot_name: str


sub_det_cols = {
    "vb": Collection(branch_name="VertexBarrelCollection", plot_name="Vertex Barrel"),
    "ve": Collection(branch_name="VertexEndcapCollection", plot_name="Vertex Endcap"),
}

key_mapping = {
    ".position.x": "x",
    ".position.y": "y",
    ".position.z": "z",
}


def getArgumentNameSpace() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputFiles",
        "-f",
        default=[fspath(inputFileDefault)],
        type=list,
        help="relative path to the input file",
    )
    return parser.parse_args()


def getPositionsAndTime(
    args: argparse.Namespace,
) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    pos = {}
    time = {}
    with uproot.open(args.inputFiles[0] + ":events") as events:
        for sub_det_key, sub_det_name in sub_det_cols.items():
            branch_base_name = sub_det_name.branch_name + "/" + sub_det_name.branch_name
            iter_cols = iter(key_mapping)
            pos[sub_det_key] = events.arrays(
                [
                    branch_base_name + next(iter_cols),
                    branch_base_name + next(iter_cols),
                    branch_base_name + next(iter_cols),
                ],
                library="np",
            )
            time[sub_det_key] = events[
                "VertexBarrelCollection/VertexBarrelCollection.time"
            ].array(library="np")
            # Renaming keys in place
            for old_key, new_key in key_mapping.items():
                pos[sub_det_key][new_key] = pos[sub_det_key].pop(
                    branch_base_name + old_key
                )

            # Flatten the arrays
            pos[sub_det_key] = flatten_first_entry(pos[sub_det_key])
            time[sub_det_key] = flatten_first_entry(time[sub_det_key])
    return pos, time


def flatten_first_entry(
    data: Union[Dict[str, np.ndarray], np.ndarray]
) -> Union[Dict[str, np.ndarray], np.ndarray]:
    """
    Replace each array of arrays with the first nested array.

    Parameters:
    - data (dict or np.ndarray): A dictionary with numpy arrays or a single numpy array.

    Returns:
    - A new dictionary or numpy array with the first nested arrays.
    """
    if isinstance(data, dict):
        # Handle the case for dictionaries like vbc_pos
        flattened_data = {}
        for key, value in data.items():
            if (
                isinstance(value, np.ndarray)
                and value[0].shape[0] > 0
                and value[1].shape[0] == 0
            ):
                # Check if it's indeed an array of arrays and non-empty
                flattened_data[key] = value[0]
            else:
                flattened_data[key] = value
        return flattened_data
    if isinstance(data, np.ndarray) and data.ndim > 1 and data.shape[0] > 0:
        # Handle the case for numpy arrays like vbc_time if similar structure
        return data[0]
    return data


def main() -> None:

    # events = getEvents(args.inputFiles)
    pos, time = getPositionsAndTime(getArgumentNameSpace())

    for sub_det_key, sub_det_name in sub_det_cols.items():

        # Plot histogram of the z positions
        plt.figure(figsize=(6, 4))
        plt.hist(pos[sub_det_key]["z"], bins=30)
        plt.title("Z Positions in " + sub_det_name.plot_name)
        plt.xlabel("Z Position")
        plt.ylabel("Frequency")
        plt.show()

        # # Plot histogram of the y positions
        # plt.figure(figsize=(6, 4))
        # plt.hist(vbc_pos["y"], bins=30)
        # plt.title("y Positions in Vertex Barrel")
        # plt.xlabel("y Position")
        # plt.ylabel("Frequency")
        # plt.show()

        # # Plot histogram of the x positions
        # plt.figure(figsize=(6, 4))
        # plt.hist(vbc_pos["x"], bins=30)
        # plt.title("x Positions in Vertex Barrel")
        # plt.xlabel("x Position")
        # plt.ylabel("Frequency")
        # plt.show()

        # Plot histogram of the times
        plt.figure(figsize=(6, 4))
        plt.hist(time[sub_det_key], bins=30)
        plt.title("Hit Time in " + sub_det_name.plot_name)
        plt.xlabel("Time")
        plt.ylabel("Frequency")
        plt.show()

        # Plot 2D histogram of the x and y positions
        plt.figure(figsize=(6, 4))
        plt.hist2d(
            pos[sub_det_key]["x"],
            pos[sub_det_key]["y"],
            bins=30,
            cmap="plasma",
            norm=mcolors.LogNorm(),
        )
        plt.title("X and Y Positions in " + sub_det_name.plot_name)
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.colorbar(label="Counts")
        plt.show()

    # #############################################
    # # experimenting
    # #############################################
    #
    # e = reader.get("events")[0]
    # vertex_barrel_collection = e.get("VertexBarrelCollection")
    # vertex_endcap_collection = e.get("VertexEndcapCollection")

    # print(vertex_barrel_collection[0].getPosition().x)
    # print(vertex_endcap_collection[0].getTime())


main()
