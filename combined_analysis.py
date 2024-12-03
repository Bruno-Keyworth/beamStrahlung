import argparse
from os import fspath
from pathlib import Path

from tabulate import tabulate

from analyze_available_data import parse_files, print_detector_info, sort_detector_data
from analyze_bs import plotting
from caching import handle_cache_operations
from platform_paths import get_home_directory
from simall import bs_data_paths
from platform_paths import resolve_path_with_env

show_plts = False
DEFAULT_DETECTOR_MODELS = [
    "ILD_FCCee_v01_fields",
    "ILD_l5_v02",
    # "ILD_FCCee_v02",
]  # Set your default detector models
DEFAULT_SCENARIOS = ["FCC091", "FCC240", "ILC250"]  # Set your default scenarios


def parse_arguments():
    homeDir = get_home_directory()

    parser = argparse.ArgumentParser(
        description="Combined Analysis of Detector Model Files"
    )
    parser.add_argument(
        "--directory",
        "-d",
        required=True,
        type=str,
        help="Directory containing the data files; can be relative to the 'dtDir' env var",
    )
    parser.add_argument(
        "--mode",
        default="overview",
        choices=["overview", "analysis", "ana_all"],
        help="Mode of operation: overview, analysis, or ana_all",
    )
    parser.add_argument(
        "--detectorModel",
        nargs="*",
        type=str,
        help="Specify one or more detector models for analysis",
    )
    parser.add_argument(
        "--scenario",
        nargs="*",
        type=str,
        choices=set(bs_data_paths),  # single source of truth
        help="Specify one or more scenarios for analysis",
    )
    parser.add_argument(
        "--cacheDir",
        default=fspath(homeDir / "promotion/data/bs_cache_combined_analysis"),
        type=str,
        help="Directory to store cache files",
    )
    parser.add_argument(
        "--savePlots", action="store_true", help="If given, plots are stored."
    )

    return parser.parse_args()


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

    # Get the position and time arrays including caching operations
    pos, time = handle_cache_operations(
        args.cacheDir, detector_model, scenario, num_bX, file_paths
    )

    plotting(
        pos,
        time,
        num_bX,  # Pass the number of bunch crossings
        show_plts,
        save_plots=args.savePlots,
        make_theta_hist=True,
        scenario=scenario,
        det_mod=detector_model,
    )


def main():

    args = parse_arguments()

    directory = resolve_path_with_env(args.directory, "dtDir")

    # Parse the files to gather detector data
    detector_data = parse_files(directory)

    if args.mode == "overview":
        print_detector_info(detector_data)
    elif args.mode == "analysis":
        # Determine which detector models and scenarios to analyze
        detector_models = args.detectorModel or DEFAULT_DETECTOR_MODELS
        scenarios = args.scenario or DEFAULT_SCENARIOS

        for detector_model in detector_models:
            if detector_model in detector_data:
                for scenario in scenarios:
                    if scenario in detector_data[detector_model]:
                        analyze_combination(directory, detector_model, scenario, args)

    elif args.mode == "ana_all":
        # Analyze all combinations of detector models and scenarios
        for detector_model in sorted(detector_data.keys()):
            for scenario in sorted(detector_data[detector_model].keys()):
                analyze_combination(directory, detector_model, scenario, args)


if __name__ == "__main__":
    main()
