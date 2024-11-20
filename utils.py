from pathlib import Path
from typing import Dict

import numpy as np


def cartesian_to_spherical(cartesian: np.ndarray) -> np.ndarray:
    """
    Convert Cartesian coordinates (x, y, z) to spherical coordinates (r, theta, phi).

    Parameters:
    -----------
    cartesian : numpy.ndarray
        A Nx3 array containing Cartesian coordinates, where each row is (x, y, z).

    Returns:
    --------
    numpy.ndarray
        A Nx3 array containing spherical coordinates:
        - r (radius)
        - theta (elevation angle) from Z-axis down (default)
        - phi (azimuth angle)

    Notes:
    ------
    To define theta (elevation) from the XY-plane up, uncomment the alternative line for theta.
    """

    # Create an empty array of shape (N, 3) to hold the spherical coordinates
    spherical = np.empty((cartesian.shape[0], 3))

    # Calculate intermediate value xy
    xy = cartesian[:, 0] ** 2 + cartesian[:, 1] ** 2

    # Fill spherical coordinates
    spherical[:, 0] = np.sqrt(xy + cartesian[:, 2] ** 2)  # radial distance (r)
    spherical[:, 1] = np.arctan2(
        np.sqrt(xy), cartesian[:, 2]
    )  # elevation angle (theta) from Z-axis down
    # spherical[:, 1] = np.arctan2(cartesian[:, 2], np.sqrt(xy))  # elevation angle (theta) from XY-plane up
    spherical[:, 2] = np.arctan2(
        cartesian[:, 1], cartesian[:, 0]
    )  # azimuth angle (phi)

    return spherical


def construct_beamstrahlung_paths(
    desy_dust_home_path, is_executed_on_desy_naf
) -> Dict[str, Dict[str, Path]]:
    """
    Returns:
    Dict[str, Dict[str, Path]]: The first key is the background scenario
                    and the second key is machine_identifier. The value
                    is the path of the data file on the chosen machine.
    """

    # must be part of the home dir path
    kek_machine_identifier = "ilc"
    desy_naf_machine_identifier = "desy.de"

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
    Retrieves the appropriate path based on the current machine's home directory.

    This function takes a dictionary `path_dict` where keys are expected
    to be identifiers for different machines (or environments), and the values
    are `Path` objects representing paths specific to those machines. It checks
    the parts of the current user's home directory path to find a match with one of
    the keys in `path_dict`.

    Parameters:
    path_dict (dict): A dictionary with machine/environment identifiers as keys
                    and `Path` objects as values.

    Returns:
    Path: The path corresponding to the current machine, as specified in `path_dict`.

    Raises:
    KeyError: If none of the keys in `path_dict` are found in the current machine's
            home directory path parts, indicating that the machine is unknown
            or not configured in `path_dict`.
    """
    path_parts = Path.home().parts
    for key in path_dict:
        if key in path_parts:
            return path_dict[key]
    raise KeyError(
        f"Machine unknown. One of the keys {list(path_dict)} has to be in {path_parts}."
    )
