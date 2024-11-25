from pathlib import Path

from det_mod_configs import get_paths_and_detector_configs
from platform_paths import (
    code_dir,
    construct_beamstrahlung_paths,
    desy_dust_home_path,
    desy_naf_machine_identifier,
    get_path_for_current_machine,
    identify_system,
)
from submit_utils_4_simall import submit_job

# Define the variables
submit_jobs = False  # Boolean variable to switch between modes

bunchCrossingEnd = 2
nEvents = 5000
guineaPigPartPerE = -1
versionName = "post_ecfa"
# FCCee
detMods2Ana = {
    "ILD_FCCee_v01",
    #    "ILD_FCCee_v01_fields",
    #    "ILD_FCCee_v01_fields_noMask",
    #    "ILD_FCCee_v02",
}
acceleratorConfigs2Ana = {"FCC091", "FCC240"}
# # ILC
# detMods2Ana = {"ILD_l5_v02", "ILD_l5_v03", "ILD_l5_v05"}
# acceleratorConfigs2Ana = {"ILC250"}

isExecutedOnDESYNAF = identify_system() == desy_naf_machine_identifier

# define paths for later use
beamStrahlungCodeDir = code_dir / "beamStrahlung"
k4geoDir = code_dir / "k4geo"
outDir = desy_dust_home_path if isExecutedOnDESYNAF else Path.home()
outDir = outDir / "promotion" / "data" / versionName  # assumption
bs_data_paths = construct_beamstrahlung_paths(desy_dust_home_path, isExecutedOnDESYNAF)

# Source the setup script (this will be a no-op in Python, since sourcing doesn't propagate in subprocess)
setupScriptPath = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

# Dict containing the detector model configurations
det_mod_configs_dict = get_paths_and_detector_configs(beamStrahlungCodeDir)


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

    outDir.mkdir(parents=True, exist_ok=True)

    # Iterate over the beam strahlung scenarios
    for bs_scenario_name in acceleratorConfigs2Ana:

        for bunchCrossing in range(1, bunchCrossingEnd + 1):
            if checkMaxBXNumberExceeded(bs_scenario_name, bunchCrossing):
                break

            bsPathWithBXNumber = replaceBXNumberInString(
                bs_scenario_name, bunchCrossing
            )

            # Iterate over the detector models
            for detModName, detModConfigs in det_mod_configs_dict.items():
                if detModName in detMods2Ana:
                    # Construct the compactFile name
                    compactFile = k4geoDir / detModConfigs.relative_compact_file_path

                    # Construct the output file names
                    outName = (
                        outDir
                        / f"{detModName}-{bs_scenario_name}-bX_{str(bunchCrossing).zfill(4)}-nEvts_{nEvents}"
                    )
                    outputFileName = outName.with_suffix(".edm4hep.root")
                    outputLogFileName = outName.with_suffix(".log")

                    # Define the executable and arguments separately
                    executable = "ddsim"
                    arguments = [
                        "--steeringFile",
                        str(detModConfigs.ddsim_file),
                        "--compactFile",
                        str(compactFile),
                        "--inputFile",
                        str(bsPathWithBXNumber),
                        "--outputFile",
                        str(outputFileName),
                        "--numberOfEvents",
                        str(nEvents),
                        "--guineapig.particlesPerEvent",
                        str(guineaPigPartPerE),
                        ">",
                        str(outputLogFileName),
                        "2>&1",
                    ]

                    # Decide whether to use Condor or bsub
                    batch_system = "condor" if isExecutedOnDESYNAF else "bsub"

                    # Submit the job using the appropriate batch system
                    submit_job(
                        batch_system, executable, arguments, outName, submit_jobs
                    )


if __name__ == "__main__":
    main()
