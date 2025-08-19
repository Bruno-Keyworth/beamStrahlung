"""
This module provides functionality to identify the current system based on the
username of the user executing the script. It utilizes a JSON configuration file to map
usernames to system name.
And further path utilities.
"""

import json
from os import getenv
from pathlib import Path
from typing import Dict

KEK_MACHINE_IDENTIFIER = "kek"
DESY_NAF_MACHINE_IDENTIFIER = "desy-naf"
SPECTRE_MACHINE_IDENTIFIER = "spectre"

SIM_DATA_SUBDIR_NAME = "sim"
MY_CODE_DIR_ENV_VAR_NAME = "codeDir"

if not getenv(MY_CODE_DIR_ENV_VAR_NAME):
    raise EnvironmentError(
        f"Environment variable '{MY_CODE_DIR_ENV_VAR_NAME}' is not set."
    )
code_dir = Path(getenv(MY_CODE_DIR_ENV_VAR_NAME))
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
    Path("/data/dust/user") / getenv("USER")
    if identify_system() == DESY_NAF_MACHINE_IDENTIFIER
    else None
)


def get_home_directory():
    if identify_system() == DESY_NAF_MACHINE_IDENTIFIER:
        return desy_dust_home_path
    return Path.home()

def construct_SR_paths(
    desy_dust_home_path, is_executed_on_desy_naf
) -> Dict[str, Dict[str, Path]]:
    """
    Returns:
    Dict[str, Dict[str, Path]]: The first key is the background scenario
                    and the second key is machine_identifier. The value
                    is the path of the data file on the chosen machine.
    """

    desy_dust_SR_base_path = (
        desy_dust_home_path / "promotion" / "data" / "split_up_SR_files"
        if is_executed_on_desy_naf
        else ""
    )

    sr_data_paths = {
        "10urad_nzco": { # 182GeV COM
            KEK_MACHINE_IDENTIFIER: Path(
                "/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"
            ),
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_SR_base_path
                / "sr_photons_from_positron_182GeVcom_nzco_10urad_v23_mediumfilter/10urad_nzco_#N"
                if desy_dust_SR_base_path
                else ""
            ),
        },
        "6urad_nzco": { # 182GeV COM
            KEK_MACHINE_IDENTIFIER: Path(
                "/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"
            ),
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_SR_base_path
                / "sr_photons_from_positron_182GeVcom_nzco_6urad_v23_mediumfilter/6urad_nzco_#N"
                if desy_dust_SR_base_path
                else ""
            ),
        },
        "2urad_nzco": { # 182GeV COM
            KEK_MACHINE_IDENTIFIER: Path(
                "/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"
            ),
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_SR_base_path
                / "sr_photons_from_positron_182GeVcom_nzco_2urad_v23_mediumfilter/2urad_nzco_#N"
                if desy_dust_SR_base_path
                else ""
            ),
        },
        "45GeV_halo": {
            KEK_MACHINE_IDENTIFIER: Path(
                "/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"
            ),
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_SR_base_path
                / "sr_photons_from_20Mpositron_45GeVcom_halo_v23_mediumfilter/45GeV_halo_#N"
                if desy_dust_SR_base_path
                else ""
            ),
        },
        "182GeV_halo": {
            KEK_MACHINE_IDENTIFIER: Path(
                "/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"
            ),
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_SR_base_path
                / "sr_photons_from_40Mpositron_182GeVcom_halo_v23_mediumfilter/182GeV_halo_#N"
                if desy_dust_SR_base_path
                else ""
            ),
        },
    }

    return sr_data_paths

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
        desy_dust_home_path / "promotion" / "data" / "split_up_beamstrahlung_files"
        if is_executed_on_desy_naf
        else ""
    )

    beam_strahlung_data_paths = {
        "ILC250": {
            KEK_MACHINE_IDENTIFIER: Path(
                "/group/ilc/users/jeans/pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.#N.pairs"
            ),
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_beamstrahlung_base_path
                / "pairs-ILC250_gt2MeV/ILC250_#N"
                if desy_dust_beamstrahlung_base_path
                else ""
            ),
        },
        "FCC091": {
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_beamstrahlung_base_path
                / "tpc-ion_tpc-bspairs_input-allatip/FCC091_#N"
                if desy_dust_beamstrahlung_base_path
                else ""
            ),
        },
        "FCC240": {
            KEK_MACHINE_IDENTIFIER: Path(
                "/home/ilc/jeans/guineaPig/fromAndrea/pairs100/allAtIP_ZH/FCC240_#N"
            ),
            DESY_NAF_MACHINE_IDENTIFIER: (
                desy_dust_beamstrahlung_base_path
                / "guineaPig_fromAndrea_pairs100_allAtIP-ZH/FCC240_#N"
                if desy_dust_beamstrahlung_base_path
                else ""
            ),
        },
    }

    return beam_strahlung_data_paths

def construct_paths(
    desy_dust_home_path, is_executed_on_desy_naf
):  
    bs_data_paths = construct_beamstrahlung_paths(desy_dust_home_path, is_executed_on_desy_naf)
    sr_data_paths = construct_SR_paths(desy_dust_home_path, is_executed_on_desy_naf)

    file_extensions = {
        "beamstrahlung" : "pairs",
        "synchrotron" : "hepevt",
    }

    return bs_data_paths, sr_data_paths, file_extensions
    


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


def resolve_path_with_env(input_path: str | Path, env_var_name: str) -> Path:
    """
    Returns an absolute Path object by combining a given path with a specified environment variable if necessary.

    This function checks whether the given path is absolute. If it is absolute, it returns the path as a Path object.
    If the path is not absolute, the function checks for the presence of the specified environment variable. If the
    environment variable is set, the function combines its value with the given relative path and returns the
    resulting absolute Path object. If the environment variable is not set, an EnvironmentError is raised.

    Parameters:
    - input_path (str or Path): The input path (string) to be processed.
    - env_var_name (str): The name of the environment variable to be used for constructing the absolute path if
      the input path is not absolute.

    Returns:
    - Path: An absolute Path object representing the combined path.

    Raises:
    - EnvironmentError: If the input path is not absolute and the specified environment variable is not set.
    """

    path = Path(input_path)

    # Check if the input path is already absolute
    if path.is_absolute():
        return path

    # Check if the specified environment variable is set
    env_var_value = getenv(env_var_name)

    if env_var_value is None:
        raise EnvironmentError(f"The environment variable '{env_var_name}' is not set.")

    # Combine the environment variable value with the provided path
    combined_path = Path(env_var_value) / path
    return combined_path
