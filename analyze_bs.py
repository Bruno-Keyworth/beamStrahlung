import argparse
from collections import defaultdict
from os import fspath
from pathlib import Path
from typing import Dict, List, Tuple, Union

import numpy as np
import uproot

from det_mod_configs import detector_model_configurations

save_plots = False
show_plts = True

inputFileDefault = (
    Path.home()
    / "promotion/data/TEST_IMPROVED/ILD_FCCee_v01"
    / "pairs-2_ZHatIP_tpcTimeKeepMC_keep_microcurlers_10MeV_30mrad_ILD_FCCee_v01.emd4hep.root"
)


key_mapping = {
    ".position.x": "x",
    ".position.y": "y",
    ".position.z": "z",
}


def get_argument_name_space() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputFiles",
        "-f",
        default=fspath(inputFileDefault),
        type=str,
        nargs="+",
        help="relative path to the input file",
    )
    return parser.parse_args()


def get_positions_and_time(
    file_paths: List[str], detector_model: str
) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    all_pos = {}
    all_time = {}
    pos = {}
    time_d = {}

    # Initialize the keys with empty lists to collect data from all files
    sub_det_cols = detector_model_configurations[
        detector_model
    ].get_sub_detector_collection_info()
    for sub_det_key in sub_det_cols.keys():
        pos[sub_det_key] = []
        time_d[sub_det_key] = []

    for file_path in file_paths:
        with uproot.open(file_path + ":events") as events:
            for sub_det_key, hit_col in sub_det_cols.items():
                branch_base_name = (
                    hit_col.root_tree_branch_name + "/" + hit_col.root_tree_branch_name
                )
                iter_cols = iter(key_mapping)
                pos_data = events.arrays(
                    [
                        branch_base_name + next(iter_cols),
                        branch_base_name + next(iter_cols),
                        branch_base_name + next(iter_cols),
                    ],
                    library="np",
                )
                time_data = events[
                    "VertexBarrelCollection/VertexBarrelCollection.time"
                ].array(library="np")

                # Renaming keys in place
                for old_key, new_key in key_mapping.items():
                    pos_data[new_key] = pos_data.pop(branch_base_name + old_key)

                # Flatten the arrays
                pos_data = flatten_first_entry(pos_data)
                time_data = flatten_first_entry(time_data)
                time_data = time_data[0]

                # Append to the respective list
                pos[sub_det_key].append(pos_data)
                time_d[sub_det_key].append(time_data)

    for sub_det_key, file_list in pos.items():  # keys vb, ve
        all_pos[sub_det_key] = dict(
            (k, [d[k] for d in file_list]) for k in file_list[0]
        )
        for keyy, lis in all_pos[sub_det_key].items():
            all_pos[sub_det_key][keyy] = np.concatenate(lis)

    for sub_det_key, file_list in time_d.items():
        all_time[sub_det_key] = np.concatenate(time_d[sub_det_key])

    return all_pos, all_time


def get_p_n_t(
    file_paths: List[str], detector_model: str
) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:

    pos_n_t = defaultdict(lambda: defaultdict(list))

    my_key_mapping = {
        ".position.x": "x",
        ".position.y": "y",
        ".position.z": "z",
        ".time": "t",
    }

    sub_det_cols = detector_model_configurations[
        detector_model
    ].get_sub_detector_collection_info()

    for sub_det_key, hit_col in sub_det_cols.items():
        alis = {
            value: f"{hit_col.root_tree_branch_name}{key}"
            for key, value in my_key_mapping.items()
        }

        # uproot.concatenate not used as depends on available/needed memory
        for batch in uproot.iterate(
            [{fp: "events"} for fp in file_paths],
            list(alis.keys()),
            library="np",
            aliases=alis,
        ):
            for observable_key in alis.keys():
                pos_n_t[sub_det_key][observable_key].append(batch[observable_key])

    # Flattening the dict entries
    for sub_det_key, observables in pos_n_t.items():
        for observable_key, arrays in observables.items():
            # Concatenate the arrays and flatten in case of multi-dimensional arrays
            # 1. Concatenation: due to several files and list in defaultdict
            concatenated_array = (
                np.concatenate(arrays) if len(arrays) > 1 else arrays[0]
            )
            # 2. Concatenation: due to several events in a root file resulting in nested ndarrays
            observables[observable_key] = (
                np.concatenate(concatenated_array)
                if isinstance(
                    concatenated_array[0], np.ndarray
                )  # testing only 0th entry should be fine as above concat. enforces same datatype
                else concatenated_array
            )

    return dict(pos_n_t)


def flatten_first_entry(
    data: Union[Dict[str, np.ndarray], np.ndarray],
) -> Union[Dict[str, np.ndarray], np.ndarray]:
    """
    Replace each array of arrays with the first nested array.

    Parameters:
    - data (dict or np.ndarray): A dictionary with numpy arrays or a single numpy array.

    Returns:
    - A new dictionary or numpy array with the first nested arrays.
    """
    if isinstance(data, dict):
        # Handle the case for dictionaries like pos
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
