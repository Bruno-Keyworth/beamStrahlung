import argparse
from pathlib import Path

from det_mod_configs import (
    CHOICES_DETECTOR_MODELS,
    DEFAULT_DETECTOR_MODELS,
    get_paths_and_detector_configs,
)
from platform_paths import (
    code_dir,
    construct_beamstrahlung_paths,
    desy_dust_home_path,
    desy_naf_machine_identifier,
    get_path_for_current_machine,
    identify_system,
)
from submit_utils_4_simall import submit_job

isExecutedOnDESYNAF = identify_system() == desy_naf_machine_identifier

# define paths for later use
beamStrahlungCodeDir = code_dir / "beamStrahlung"
k4geoDir = code_dir / "k4geo"
out_Dir_base_path = desy_dust_home_path if isExecutedOnDESYNAF else Path.home()
bs_data_paths = construct_beamstrahlung_paths(desy_dust_home_path, isExecutedOnDESYNAF)

# single source of truth, keys of bs_data_paths become values of tuple
CHOICES_SCENARIOS = tuple(bs_data_paths)
DEFAULT_SCENARIOS = "FCC240"

# Source the setup script (this will be a no-op in Python, since sourcing doesn't propagate in subprocess)
setupScriptPath = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

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
        "--versionName",
        "-v",
        type=str,
        required=True,
        help="Version name for the simulation",
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


def replaceBXNumberInString(bsTypeName: str, bxN: int) -> str:
    if bsTypeName == "ILC250":
        return str(get_path_for_current_machine(bs_data_paths[bsTypeName])).replace(
            "#N", str(bxN).zfill(4)
        )
    return str(get_path_for_current_machine(bs_data_paths[bsTypeName])).replace(
        "#N", str(bxN)
    )


def checkMaxBXNumberExceeded(bsTypeName: str, bunchCrossing: int) -> bool:
    """
    Check whether maximum number of bunch crossings per beam strahlung type is exceeded.
    """
    if bsTypeName in {"FCC240", "FCC091"} and bunchCrossing > 100:
        print(
            f"\nThere are only 100 bunch crossing for {bsTypeName} available",
            end="\n\n",
        )
        return True
    if bsTypeName == "ILC250" and bunchCrossing > 1312:
        print(
            f"\nThere are only 1312 bunch crossing for {bsTypeName} available",
            end="\n\n",
        )
        return True
    return False


def main():
    # # Function to simulate sourcing (can only be done inside the same shell process)
    # def source_setup_script(script):
    #     return subprocess.run(
    #         f"source {script} && env", shell=True, capture_output=True, text=True
    #     )

    # # Note: The setup script source cannot affect the Python environment, but we simulate it in case needed.
    # source_setup_script(setupScriptPath)  # This will not affect the Python environment

    args = parse_arguments()
    outDir = out_Dir_base_path / "promotion" / "data" / args.versionName  # assumption
    outDir.mkdir(parents=True, exist_ok=True)

    # Iterate over the beam strahlung scenarios
    for bs_scenario_name in args.scenario:
        for bunchCrossing in range(1, args.bunchCrossingEnd + 1):
            if checkMaxBXNumberExceeded(bs_scenario_name, bunchCrossing):
                break

            bsPathWithBXNumber = replaceBXNumberInString(
                bs_scenario_name, bunchCrossing
            )

            # Iterate over the detector models
            for detModName, detModConfigs in det_mod_configs_dict.items():
                if detModName in args.detectorModel:

                    # Construct the output file names
                    outName = (
                        outDir
                        / f"{detModName}-{bs_scenario_name}-bX_{str(bunchCrossing).zfill(4)}-nEvts_{args.nEvents}"
                    )

                    # Define the executable and arguments separately
                    executable = "ddsim"
                    arguments = [
                        "--steeringFile",
                        str(beamStrahlungCodeDir / detModConfigs.get_ddsim_file_path()),
                        "--compactFile",
                        str(k4geoDir / detModConfigs.get_compact_file_path()),
                        "--inputFile",
                        str(bsPathWithBXNumber),
                        "--outputFile",
                        str(outName.with_suffix(".edm4hep.root")),
                        "--numberOfEvents",
                        str(args.nEvents),
                        "--guineapig.particlesPerEvent",
                        str(args.guineaPigPartPerE),
                    ]

                    # Decide whether to use Condor or bsub
                    batch_system = "condor" if isExecutedOnDESYNAF else "bsub"

                    # Submit the job using the appropriate batch system
                    submit_job(
                        batch_system,
                        arguments,
                        outName,
                        args.submit_jobs,
                        beamStrahlungCodeDir,
                        executable,
                    )


if __name__ == "__main__":
    main()
