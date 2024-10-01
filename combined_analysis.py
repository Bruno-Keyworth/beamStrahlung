import argparse
from pathlib import Path
from collections import defaultdict
from analyze_available_data import (
    parse_files,
    print_detector_info,
)  # Import from the old script

# from analyze_bs import getPositionsAndTime  # Import from the generated script

DEFAULT_DETECTOR_MODEL = "ILD_l5_v02"  # Set your default detector model
DEFAULT_SCENARIO = "ILC250"  # Set your default scenario


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
        choices=["overview", "analysis"],
        help="Mode of operation: overview or analysis",
    )
    parser.add_argument(
        "--detector-model", type=str, help="Specify the detector model for analysis"
    )
    parser.add_argument(
        "--scenario", type=str, help="Specify the scenario for analysis"
    )

    args = parser.parse_args()

    # Parse the files to gather detector data
    detector_data = parse_files(args.directory)

    if args.mode == "overview":
        print_detector_info(detector_data)
    elif args.mode == "analysis":
        # Set defaults if not provided
        detector_model = (
            args.detector_model if args.detector_model else DEFAULT_DETECTOR_MODEL
        )
        scenario = args.scenario if args.scenario else DEFAULT_SCENARIO

        # Check if the specified combination exists in the detector data
        if (
            detector_model not in detector_data
            or scenario not in detector_data[detector_model]
        ):
            raise ValueError(
                f"No files found for the combination: Detector Model='{detector_model}', Scenario='{scenario}'"
            )

        # Analyze all bX Numbers for the found combination
        bX_numbers = detector_data[detector_model][scenario]
        for bX_number in bX_numbers:
            file_path = (
                Path(args.directory)
                / f"{detector_model}-{scenario}-{bX_number}-some_other_info.edm4hep.root"
            )
            #            getPositionsAndTime(file_path)  # Call the imported analyze_data function
            print(
                f"Analyzing data from file: {file_path}"
            )  # Log the file being analyzed


if __name__ == "__main__":
    main()
