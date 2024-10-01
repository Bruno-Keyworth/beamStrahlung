import argparse
from pathlib import Path
from collections import defaultdict
from tabulate import tabulate

def parse_files(directory):
    detector_data = defaultdict(lambda: defaultdict(set))

    # Iterate over all .edm4hep.root files in the provided directory
    for file_path in Path(directory).rglob('*.edm4hep.root'):
        # Extract components of the filename
        parts = file_path.stem.split('-')

        if len(parts) != 4:
            continue  # Skip any files that don't match the expected format

        detector_model = parts[0]
        scenario = parts[1]
        bX_number = parts[2]  # bX_Number
        e_number = parts[3].split('_')[-1]  # Extract ENumber from the last part
        
        # Add the bX_Number to the appropriate detector_model and scenario
        detector_data[detector_model][scenario].add(bX_number)

    return detector_data

def print_detector_info(detector_data):
    table_data = []

    # Sort the detector models
    for detector_model in sorted(detector_data.keys()):
        scenarios = detector_data[detector_model]
        for scenario, bX_numbers in scenarios.items():
            num_files = len(bX_numbers)
            table_data.append([detector_model, scenario, num_files])

    # Print the table using tabulate
    print(tabulate(table_data, headers=["Detector Model", "Scenario", "Different Number of Files"], tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser(description='Analyze detector model files')
    parser.add_argument('directory', type=str, help='Directory containing the detector model files')

    args = parser.parse_args()

    # Parse files to gather required information
    detector_data = parse_files(args.directory)

    # Print detector model info
    print_detector_info(detector_data)

if __name__ == "__main__":
    main()
