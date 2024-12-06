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


def add_spherical_coordinates_in_place(position_dict: dict) -> None:
    """
    Convert Cartesian coordinates to spherical coordinates and add them in-place to the input dictionary.

    Parameters:
    -----------
    position_dict : dict
        A dictionary containing 'x', 'y', and 'z' as keys with numpy array values.

    Modifies:
    ---------
    The input dictionary is modified in-place to include three additional keys:
    - 'r' for radial distance
    - 'theta' for elevation angle from the Z-axis down
    - 'phi' for azimuth angle
    """
    # Combine x, y, z arrays into a single Nx3 Cartesian coordinates array
    cartesian = np.column_stack(
        (position_dict["x"], position_dict["y"], position_dict["z"])
    )

    # Use the cartesian_to_spherical function to compute spherical coordinates
    spherical = cartesian_to_spherical(cartesian)

    # Add the spherical coordinates to the dictionary in-place
    position_dict["r"] = spherical[:, 0]
    position_dict["theta"] = spherical[:, 1]
    position_dict["phi"] = spherical[:, 2]


def make_keys_uniform_length(original_dict):
    """
    Adjusts all keys in the dictionary to have the same length by appending underscores.

    Parameters:
    - original_dict (dict): The dictionary with keys to be adjusted.

    Returns:
    - dict: A new dictionary with keys of uniform length.
    """
    # Find the length of the longest key
    max_key_length = max(len(key) for key in original_dict)

    # Create a new dictionary with keys of uniform length by appending underscores
    uniform_keys_dict = {
        key.ljust(max_key_length, "_"): value for key, value in original_dict.items()
    }

    return uniform_keys_dict
