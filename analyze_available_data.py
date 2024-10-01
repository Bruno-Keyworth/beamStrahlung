import argparse
from pathlib import Path
from collections import defaultdict
from tabulate import tabulate

"""
This script analyzes detector model files following a specific naming convention.

The expected file naming format is:
DETECTOR_MODEL-SCENARIO-bX_NUMBER-nEvts_ENUMBER.edm4hep.root

The script scans a directory for files that match this format, organizes the 
data by detector model and scenario, and counts the number of different 
bX_NUMBER files found for each scenario within each detector model.

Usage:
    python analyze_detectors.py --directory <directory>  # or -d <directory>

Arguments:
    <directory>  Path to the directory containing the detector model files.
"""

def parse_files(directory):
    """
    Parse the specified directory for files that match the expected naming format.

    The expected filename format is:
    DETECTOR_MODEL-SCENARIO-bX_NUMBER-nEvts_ENUMBER.edm4hep.root

    Parameters:
    directory (str): The directory to scan for files.

    Returns:
    defaultdict: A nested dictionary containing detector models as keys,
                 scenarios as subkeys, and sets of bX numbers as values.
    """
    detector_data = defaultdict(lambda: defaultdict(set))

    # Iterate over all .edm4hep.root files in the provided directory
    for file_path in Path(directory).rglob("*.edm4hep.root"):
        # Extract components of the filename
        parts = file_path.stem.split("-")

        if len(parts) != 4:
            continue  # Skip any files that don't match the expected format

        detector_model = parts[0]
        scenario = parts[1]
        bX_number = parts[2]
        e_number = parts[3].split("_")[-1]

        # Add the bX_Number to the appropriate detector_model and scenario
        detector_data[detector_model][scenario].add(bX_number)

    return detector_data


def sort_detector_data(detector_data):
    """
    Sort the detector data by detector model, scenario, and bX numbers.

    Parameters:
    detector_data (defaultdict): The nested dictionary containing detector
                                  models, scenarios, and their corresponding bX numbers.

    Returns:
    sorted_data (defaultdict): A sorted nested defaultdict.
    """
    sorted_data = defaultdict(lambda: defaultdict(list))

    # Sort the detector models
    for detector_model in sorted(detector_data.keys()):
        scenarios = detector_data[detector_model]
        
        # Sort scenarios for the current detector model
        for scenario in sorted(scenarios.keys()):
            bX_numbers = sorted(scenarios[scenario])  # Sort bX_numbers
            sorted_data[detector_model][scenario] = bX_numbers

    return sorted_data


def print_detector_info(sorted_detector_data):
    """
    Print a table of detector information, including models, scenarios,
    and the count of different files found for each scenario.

    Parameters:
    sorted_detector_data (defaultdict): The sorted nested dictionary containing detector
                                        models, scenarios, and their corresponding bX numbers.
    """
    table_data = []

    # Prepare the table data
    for detector_model in sorted(sorted_detector_data.keys()):
        scenarios = sorted_detector_data[detector_model]

        # Iterate over the scenarios for the current detector model
        for scenario in scenarios.keys():
            bX_numbers = scenarios[scenario]
            num_files = len(bX_numbers)
            table_data.append([detector_model, scenario, num_files])

    # Print the table using tabulate
    print(
        tabulate(
            table_data,
            headers=["Detector Model", "Scenario", "Different Number of Files"],
            tablefmt="grid",
        )
    )


def main():
    """
    Main function to execute the script.

    It parses command line arguments, prints the expected filename format,
    processes the files in the given directory, and displays the results in a table format.
    """
    parser = argparse.ArgumentParser(description="Analyze detector model files")
    parser.add_argument(
        "--directory",
        "-d",
        dest="directory",
        type=str,
        help="Directory containing the detector model files",
    )

    args = parser.parse_args()

    # Print expected file naming format
    print(
        "Expected file naming format: DETECTOR_MODEL-SCENARIO-bX_NUMBER-nEvts_ENUMBER.edm4hep.root"
    )

    # Parse files to gather required information
    detector_data = parse_files(args.directory)

    # Sort the detector data
    sorted_detector_data = sort_detector_data(detector_data)

    # Print detector model info
    print_detector_info(sorted_detector_data)


if __name__ == "__main__":
    main()
