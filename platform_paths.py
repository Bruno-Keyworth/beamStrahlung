"""
This module provides functionality to identify the current system based on the
username of the user executing the script. It utilizes a JSON configuration file to map
usernames to system name. 
"""

import json
from os import getenv
from pathlib import Path
from typing import Dict

kek_machine_identifier = "kek"
desy_naf_machine_identifier = "desy-naf"
spectre_machine_identifier = "spectre"

code_dir = Path(getenv("myCodeDir"))
config_file_path = code_dir / "beamStrahlung" / "uname_to_sys_map.json"


class UnknownSystemError(Exception):
    """Custom exception raised when the system cannot be identified."""


def load_user_to_system_mapping(filepath: str) -> dict:
    """
    Loads the user-to-system mapping from a JSON configuration file.

    Args:
        filepath (str): The path to the JSON configuration file.

    Returns:
        dict: A dictionary mapping usernames to system names.

    Raises:
        FileNotFoundError: If the specified configuration file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def identify_system() -> str:
    """
    Identifies the current system based on the username from environment variables
    and a configuration file mapping.

    Args:
        config_filepath (str): The path to the JSON configuration file.

    Returns:
        str: The name of the system associated with the current username.

    Raises:
        UnknownSystemError: If the username is not recognized or the 'USER' environment
        variable is not set.
        FileNotFoundError: If the specified configuration file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    user_to_system = load_user_to_system_mapping(config_file_path)

    current_user = getenv("USER")

    if current_user is None:
        raise UnknownSystemError("The USER environment variable is not set.")

    if current_user not in user_to_system:
        raise UnknownSystemError(f"Unknown system for user: {current_user}")

    return user_to_system[current_user]


desy_dust_home_path = (
    Path("/nfs/dust/ilc/user/") / getenv("USER")
    if identify_system() == desy_naf_machine_identifier
    else None
)


def get_home_directory():
    if identify_system() == desy_naf_machine_identifier:
        return desy_dust_home_path
    return Path.home()


def construct_beamstrahlung_paths(
    desy_dust_home_path, is_executed_on_desy_naf
) -> Dict[str, Dict[str, Path]]:
    """
    Returns:
    Dict[str, Dict[str, Path]]: The first key is the background scenario
                    and the second key is machine_identifier. The value
                    is the path of the data file on the chosen machine.
    """

    desy_dust_beamstrahlung_base_path = (
        desy_dust_home_path / "beamStrahlungDataFromDaniel"
        if is_executed_on_desy_naf
        else ""
    )

    beam_strahlung_data_paths = {
        "ILC250": {
            kek_machine_identifier: Path(
                "/group/ilc/users/jeans/pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.#N.pairs"
            ),
            desy_naf_machine_identifier: (
                desy_dust_beamstrahlung_base_path
                / "pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.#N.pairs"
                if desy_dust_beamstrahlung_base_path
                else ""
            ),
        },
        "FCC091": {
            kek_machine_identifier: Path(
                "/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"
            ),
            desy_naf_machine_identifier: (
                desy_dust_beamstrahlung_base_path
                / "tpc-ion_tpc-bspairs_input-allatip/pairs-#N_Z.pairs"
                if desy_dust_beamstrahlung_base_path
                else ""
            ),
        },
        "FCC240": {
            kek_machine_identifier: Path(
                "/home/ilc/jeans/guineaPig/fromAndrea/pairs100/allAtIP_ZH/pairs-#N_ZH.pairs"
            ),
            desy_naf_machine_identifier: (
                desy_dust_beamstrahlung_base_path
                / "guineaPig_fromAndrea_pairs100_allAtIP-ZH/pairs-#N_ZH.pairs"
                if desy_dust_beamstrahlung_base_path
                else ""
            ),
        },
    }

    return beam_strahlung_data_paths


def get_path_for_current_machine(path_dict: dict) -> Path:
    """
    Retrieves the appropriate path based on the current machine's identifier.

    This function utilizes the `identify_system` function to determine the current
    machine's identifier and then retrieves the appropriate path from the given `path_dict`.

    Parameters:
    path_dict (dict): A dictionary with system identifiers as keys and `Path` objects as values.

    Returns:
    Path: The path corresponding to the current machine, as specified in `path_dict`.

    Raises:
    UnknownSystemError: If the system identifier returned by `identify_system()` does not
                         match any key in `path_dict`, indicating that the machine is
                         unknown or not configured.
    """
    system_key = identify_system()

    if system_key in path_dict:
        return path_dict[system_key]

    raise UnknownSystemError(
        f"Machine unknown. The system identifier '{system_key}' is not configured in the provided path dictionary."
    )
