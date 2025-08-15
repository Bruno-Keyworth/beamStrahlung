import argparse
from pathlib import Path
import os

from det_mod_configs import (
    CHOICES_DETECTOR_MODELS,
    DEFAULT_DETECTOR_MODELS,
    get_paths_and_detector_configs,
)
from platform_paths import (
    DESY_NAF_MACHINE_IDENTIFIER,
    SIM_DATA_SUBDIR_NAME,
    code_dir,
    construct_paths,
    desy_dust_home_path,
    get_path_for_current_machine,
    identify_system,
)
from submit_utils_4_simall import submit_job
is_executed_on_DESY_NAF = identify_system() == DESY_NAF_MACHINE_IDENTIFIER

# define paths for later use
beamstrahlung_code_dir = code_dir / "beamStrahlung"
k4geoDir = code_dir / "k4geo"
out_Dir_base_path = desy_dust_home_path if is_executed_on_DESY_NAF else Path.home()
bs_data_paths, sr_data_paths = construct_paths(
    desy_dust_home_path, is_executed_on_DESY_NAF
)

# single source of truth, keys of bs_data_paths become values of tuple
CHOICES_SCENARIOS = tuple(sr_data_paths)
DEFAULT_SCENARIOS = ("182GeVcom_nzco_10urad",)

# Source the setup script (this will be a no-op in Python, since sourcing doesn't propagate in subprocess)
SETUP_SCRIPT_PATH = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

# Dict containing the detector model configurations
det_mod_configs_dict = get_paths_and_detector_configs()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process simulation parameters for FCCee and ILC."
    )

    parser.add_argument(
        "--bunchCrossingEnd",
        type=int,
        default=2,
        help="End value for bunch crossing (default: 2)",
    )

    parser.add_argument(
        "--nEvents",
        type=int,
        default=5000,
        help="Number of events to simulate (default: 5000)",
    )

    parser.add_argument(
        "--guineaPigPartPerE",
        type=int,
        default=-1,
    )

    parser.add_argument(
        "--version",
        type=str,
        required=True,
        help="Version name for the simulation",
    )

    parser.add_argument(
        "--background",
        type=str,
        default="beamstrahlung",
        choices=("beamstrahlung", "synchrotron"),
        help="Type of background data to read"
    )

    parser.add_argument(
        "--detectorModel",
        choices=CHOICES_DETECTOR_MODELS,
        nargs="+",
        default=DEFAULT_DETECTOR_MODELS,
        help="Detector models to analyze (choose one or more)",
    )

    parser.add_argument(
        "--scenario",
        choices=CHOICES_SCENARIOS,
        nargs="+",
        default=DEFAULT_SCENARIOS,
        help="Accelerator configurations to analyze (choose one or more)",
    )

    parser.add_argument(
        "--submit_jobs", action="store_true", help="Submit job(s) if this flag is set"
    )

    return parser.parse_args()


def replace_BX_number_in_string(type_name: str, BX_n: int, background: str) -> str:

    if background == "beamstrahlung":
        data_paths = bs_data_paths
    else:
        data_paths = sr_data_paths

    if type_name == "ILC250":
        return str(get_path_for_current_machine(data_paths[type_name])).replace(
            "#N", str(BX_n).zfill(4)
        )
    return str(get_path_for_current_machine(data_paths[type_name])).replace(
        "#N", str(BX_n)
    )


def check_max_BX_number_exceeded(bs_type_name: str, bunchcrossing: int) -> bool:
    """
    Check whether maximum number of bunch crossings per beam strahlung type is exceeded.
    """
    if bs_type_name in {"FCC240", "FCC091"} and bunchcrossing > 450:
        print(
            f"\nThere are only 100 bunch crossing for {bs_type_name} available",
            end="\n\n",
        )
        return True
    if bs_type_name == "ILC250" and bunchcrossing > 1312:
        print(
            f"\nThere are only 1312 bunch crossing for {bs_type_name} available",
            end="\n\n",
        )
        return True
    return False

def save_bX_count(scenario, background, out_dir):

    first_bx_path = replace_BX_number_in_string(scenario, 1, background)
    if os.path.exists(first_bx_path):
        input_folder = os.path.dirname(first_bx_path)
        if background == "synchrotron":
            num_bx = 1
        else:
            num_bx = len([
                f for f in os.listdir(input_folder)
                if os.path.isfile(os.path.join(input_folder, f))
            ])
        bx_count_file = out_dir / f"{scenario}_number_of_bx.txt"
        with open(bx_count_file, "w") as f:
            f.write(f"{num_bx}\n")
    else:
        print(f"⚠️ No files found for scenario {scenario}, skipping count.")

def main():
    # # Function to simulate sourcing (can only be done inside the same shell process)
    # def source_setup_script(script):
    #     return subprocess.run(
    #         f"source {script} && env", shell=True, capture_output=True, text=True
    #     )

    # # Note: The setup script source cannot affect the Python environment, but we simulate it in case needed.
    # source_setup_script(setupScriptPath)  # This will not affect the Python environment

    args = parse_arguments()
    out_dir = (
        out_Dir_base_path / "promotion" / "data" / SIM_DATA_SUBDIR_NAME / args.version
    )  # assumption
    out_dir.mkdir(parents=True, exist_ok=True)

    det_mod_configs_dict_filtered = {
        key: value
        for key, value in det_mod_configs_dict.items()
        if key in args.detectorModel
    }

    # Iterate over the beam strahlung scenarios
    for bs_scenario_name in args.scenario:

        save_bX_count(bs_scenario_name, args.background, out_dir)

        # loop over different files, bX is file index
        for bunchcrossing in range(1, args.bunchCrossingEnd + 1):

            bs_path_with_BX_number = replace_BX_number_in_string(
                bs_scenario_name, bunchcrossing, args.background
            )
            if not os.path.exists(bs_path_with_BX_number):
                print(
                    f"\nThere are only {bunchcrossing-1} files for {bs_scenario_name} available",
                    end="\n\n",
                )
                break

            # Iterate over the detector models
            for det_mod_name, det_mod_configs in det_mod_configs_dict_filtered.items():
                # Construct the output file names
                out_name = (
                    out_dir
                    / f"{det_mod_name}-{bs_scenario_name}-bX_{str(bunchcrossing).zfill(4)}-nEvts_{args.nEvents}"
                )

                print(bs_path_with_BX_number)

                # Define the executable and arguments separately
                executable = "ddsim"
                arguments = [
                    "--steeringFile",
                    str(beamstrahlung_code_dir / "ddsim_keep_microcurlers_10MeV.py"),
                    "--compactFile",
                    str(k4geoDir / det_mod_configs.get_compact_file_path()),
                    "--inputFile",
                    str(bs_path_with_BX_number),
                    "--outputFile",
                    str(out_name.with_suffix(".edm4hep.root")),
                    "--numberOfEvents",
                    str(args.nEvents),
                    "--crossingAngleBoost",
                    str(det_mod_configs.get_crossing_angle()),
                ]

                if det_mod_configs.is_accelerator_ilc:
                    # increased resources needed
                    more_resources = True
                    # Determine particles per event value for "ILC" scenario
                    particles_per_event = (
                        str(args.guineaPigPartPerE)
                        if 1 <= args.guineaPigPartPerE <= 5000
                        else str(5000)
                    )
                else:
                    # Use the provided particles per event for non-"ILC" scenarios
                    particles_per_event = str(args.guineaPigPartPerE)

                # Add particles per event argument
                arguments.extend(
                    [
                        "--guineapig.particlesPerEvent",
                        particles_per_event,
                    ]
                )

                # Decide whether to use Condor or bsub
                batch_system = "condor" if is_executed_on_DESY_NAF else "bsub"

                # Submit the job using the appropriate batch system
                submit_job(
                    batch_system,
                    arguments,
                    out_name,
                    args.submit_jobs,
                    beamstrahlung_code_dir,
                    executable,
                    more_rscrs=more_resources,
                )


if __name__ == "__main__":
    main()
