import argparse
import pickle
from os import fspath
from pathlib import Path

from tabulate import tabulate

from analyze_available_data import parse_files, print_detector_info, sort_detector_data
from analyze_bs import getPositionsAndTime, plotting

show_plts = True
save_plots = False
DEFAULT_DETECTOR_MODEL = "ILD_FCCee_v01"  # Set your default detector model
DEFAULT_SCENARIO = "FCC91"  # Set your default scenario


def get_cache_filename(cache_dir, detector_model, scenario, num_bX):
    """Generate a unique cache filename based on the detector model, scenario, and number of bXs."""
    return f"{cache_dir}/cache_{detector_model}_{scenario}_{num_bX}.pkl"


def load_from_cache(cache_file):
    """Load data from cache if it exists."""
    if cache_file.exists():
        with cache_file.open("rb") as f:
            return pickle.load(f)
    return None


def save_to_cache(cache_file, data):
    """Save data to cache."""
    with cache_file.open("wb") as f:
        pickle.dump(data, f)


def analyze_combination(directory, detector_model, scenario, args):
    """Analyze a specific combination of detector model and scenario."""

    # Sort detector data
    detector_data = sort_detector_data(parse_files(directory))

    if (
        detector_model not in detector_data
        or scenario not in detector_data[detector_model]
    ):
        raise ValueError(
            f"No files found for the combination: Detector Model='{detector_model}', Scenario='{scenario}'"
        )

    # Get the list of bX identifiers (bunch crossing identifiers)
    bX_identifiers = detector_data[detector_model][scenario]

    # Determine the number of bunch crossings
    num_bX = len(bX_identifiers)

    # Prepare file paths
    file_paths = [
        fspath(
            Path(directory)
            / f"{detector_model}-{scenario}-{bX_identifier}-nEvts_5000.edm4hep.root"
        )
        for bX_identifier in bX_identifiers
    ]

    # Print current combination in a grid table format
    table_data = [[detector_model, scenario, num_bX]]
    print(
        tabulate(
            table_data,
            headers=["Detector Model", "Scenario", "Num Bunch Crossings"],
            tablefmt="grid",
        )
    )

    # Cache-related operations
    cache_file = Path(
        get_cache_filename(args.cacheDir, detector_model, scenario, num_bX)
    )
    cached_data = load_from_cache(cache_file)

    if cached_data is not None:
        pos, time = cached_data
        print(
            f"Loaded data for Detector Model='{detector_model}', Scenario='{scenario}' from cache."
        )
    else:
        pos, time = getPositionsAndTime(file_paths)
        save_to_cache(cache_file, (pos, time))
        print(
            f"Data loaded and cached for Detector Model='{detector_model}', Scenario='{scenario}'."
        )

    plotting(
        pos,
        time,
        num_bX,  # Pass the number of bunch crossings
        show_plts,
        save_plots=save_plots,
        scenario=scenario,
        det_mod=detector_model,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Combined Analysis of Detector Model Files"
    )
    parser.add_argument(
        "--directory",
        required=True,
        type=str,
        help="Directory containing the detector model files",
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["overview", "analysis", "ana_all"],
        help="Mode of operation: overview, analysis, or ana_all",
    )
    parser.add_argument(
        "--detectorModel", type=str, help="Specify the detector model for analysis"
    )
    parser.add_argument(
        "--scenario", type=str, help="Specify the scenario for analysis"
    )
    parser.add_argument(
        "--cacheDir",
        default=fspath(Path.home() / "promotion/data/bs_cache_combined_analysis"),
        type=str,
        help="Directory to store cache files",
    )

    args = parser.parse_args()

    # Use pathlib to ensure the cache directory exists
    cache_dir_path = Path(args.cacheDir)
    cache_dir_path.mkdir(parents=True, exist_ok=True)

    # Parse the files to gather detector data
    detector_data = parse_files(args.directory)

    if args.mode == "overview":
        print_detector_info(detector_data)
    elif args.mode == "analysis":
        # Set defaults if not provided
        detector_model = (
            args.detectorModel if args.detectorModel else DEFAULT_DETECTOR_MODEL
        )
        scenario = args.scenario if args.scenario else DEFAULT_SCENARIO

        analyze_combination(args.directory, detector_model, scenario, args)

    elif args.mode == "ana_all":
        for detector_model in sorted(detector_data.keys()):
            for scenario in sorted(detector_data[detector_model].keys()):
                analyze_combination(args.directory, detector_model, scenario, args)


if __name__ == "__main__":
    main()
