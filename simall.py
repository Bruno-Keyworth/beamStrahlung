import subprocess
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

# Define the variables
executeBsub = False  # Boolean variable to switch between modes

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
    check whether maximum number of bunch crossings per beam strahlung type is exceeded
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

                    # Construct the command
                    command = f"ddsim --steeringFile {detModConfigs.ddsim_file} --compactFile {compactFile} --inputFile {bsPathWithBXNumber} --outputFile {outputFileName} --numberOfEvents {nEvents} --guineapig.particlesPerEvent {guineaPigPartPerE} > {outputLogFileName} 2>&1"
                    bsub_command = f'bsub -q l "{command}"'

                    # Execute or print the command depending on executeBsub
                    if executeBsub:
                        subprocess.run(bsub_command, shell=True, check=True)
                    else:
                        print(bsub_command, end="\n\n")


if __name__ == "__main__":
    main()
