import argparse
from dataclasses import dataclass
from os import fspath
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# import awkward as ak
import uproot

inputFileDefault = (
    Path.home()
    / "promotion/data/TEST_IMPROVED/ILD_FCCee_v01/pairs-2_ZHatIP_tpcTimeKeepMC_keep_microcurlers_10MeV_30mrad_ILD_FCCee_v01.emd4hep.root"
    # / "promotion/data/TEST_IMPROVED/ILD_FCCee_v01/pairs-1_ZHatIP_tpcTimeKeepMC_keep_microcurlers_10MeV_30mrad_ILD_FCCee_v01.slcio"
)


# Define the dataclass
@dataclass
class Collection:
    branch_name: str
    plot_name: str


cols = {
    "vb": Collection(branch_name="VertexBarrelCollection", plot_name="Vertex Barrel"),
    "ve": Collection(branch_name="VertexEndcapCollection", plot_name="Vertex Endcap"),
}


def getArgumentNameSpace():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputFiles",
        "-f",
        default=[fspath(inputFileDefault)],
        type=list,
        help="relative path to the input file",
    )
    return parser.parse_args()


# def getEvents(files, events="events"):
#     return uproot.lazy([f"{fspath(f)}:{events}"] for f in files)

key_mapping = {
    "VertexBarrelCollection/VertexBarrelCollection.position.x": "x",
    "VertexBarrelCollection/VertexBarrelCollection.position.y": "y",
    "VertexBarrelCollection/VertexBarrelCollection.position.z": "z",
}


def flatten_first_entry(data):
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
    elif isinstance(data, np.ndarray) and data.ndim > 1 and data.shape[0] > 0:
        # Handle the case for numpy arrays like vbc_time if similar structure
        return data[0]
    else:
        return data


def main():

    args = getArgumentNameSpace()
    # events = getEvents(args.inputFiles)
    with uproot.open(args.inputFiles[0] + ":events") as events:
        vbc_pos = events.arrays(
            [
                "VertexBarrelCollection/VertexBarrelCollection.position.x",
                "VertexBarrelCollection/VertexBarrelCollection.position.y",
                "VertexBarrelCollection/VertexBarrelCollection.position.z",
            ],
            library="np",
        )
        vbc_time = events["VertexBarrelCollection/VertexBarrelCollection.time"].array(
            library="np"
        )
        # Renaming keys in place
        for old_key, new_key in key_mapping.items():
            vbc_pos[new_key] = vbc_pos.pop(old_key)

        # Flatten the arrays
        vbc_pos = flatten_first_entry(vbc_pos)
        vbc_time = flatten_first_entry(vbc_time)

        import time

        from IPython import embed

        embed()
        time.sleep(1)

    # Plot histogram of the z positions
    plt.figure(figsize=(6, 4))
    plt.hist(vbc_pos["z"], bins=30)
    plt.title("Z Positions in Vertex Barrel")
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
    plt.hist(vbc_time, bins=30)
    plt.title("Hit Time in Vertex Barrel")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.show()

    # Plot 2D histogram of the x and y positions
    plt.figure(figsize=(6, 4))
    h = plt.hist2d(vbc_pos["x"], vbc_pos["y"], bins=30, cmap="plasma")
    plt.title("X and Y Positions in Vertex Barrel")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.colorbar(label="Counts")
    plt.show()

    # import time

    # from IPython import embed

    # embed()
    # time.sleep(1)

    # for e in events:
    #     vertex_barrel_collection = e.get("VertexBarrelCollection")
    #     vertex_endcap_collection = e.get("VertexEndcapCollection")
    #     for vertex_barrel_hit, vertex_endcap_hit in zip(
    #         vertex_barrel_collection, vertex_endcap_collection
    #     ):
    #         print(vertex_barrel_hit.getPosition().x)
    #         print(vertex_barrel_hit.getPosition().y)
    #         print(vertex_barrel_hit.getPosition().z)
    #         print(vertex_barrel_hit.getTime())
    #         print(vertex_endcap_hit.getPosition().x)
    #         print(vertex_endcap_hit.getPosition().y)
    #         print(vertex_endcap_hit.getPosition().z)
    #         print(vertex_endcap_hit.getTime())

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
