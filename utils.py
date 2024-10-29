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
