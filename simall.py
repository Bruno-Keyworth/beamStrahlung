import subprocess
from dataclasses import dataclass
from os import getenv
from pathlib import Path

from utils import construct_beamstrahlung_paths, get_path_for_current_machine


@dataclass
class DetectorConfig:
    ddsimFile: Path
    relativeCompactFilePath: Path


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

isExecutedOnDESYNAF = "desy.de" in Path.home().parts

# define dirs to detector models
codeDir = Path(getenv("myCodeDir"))
beamStrahlungCodeDir = codeDir / "beamStrahlung"
k4geoDir = codeDir / "k4geo"
ild4FCCDir = Path("FCCee") / "ILD_FCCee" / "compact"
ild4ILCDir = Path("ILD") / "compact" / "ILD_sl5_v02"
if isExecutedOnDESYNAF:
    desyDustHomePath = Path("/nfs/dust/ilc/user/") / Path.home().parts[-1]
    outDir = desyDustHomePath
else:
    desyDustHomePath = ""
    outDir = Path.home()
outDir = outDir / "promotion" / "data" / versionName  # assumption
bs_data_paths = construct_beamstrahlung_paths(desyDustHomePath, isExecutedOnDESYNAF)

# define Paths to ddsim files
ddsim4FCC = beamStrahlungCodeDir / "ddsim_keep_microcurlers_10MeV_30mrad.py"
ddsim4ILC = beamStrahlungCodeDir / "ddsim_keep_microcurlers_10MeV.py"

# Source the setup script (this will be a no-op in Python, since sourcing doesn't propagate in subprocess)
setupScriptPath = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

# Dict containing the detector model configurations
detectorConfigs = {
    "ILD_FCCee_v01": DetectorConfig(
        ddsim4FCC, ild4FCCDir / "ILD_FCCee_v01/ILD_FCCee_v01.xml"
    ),
    "ILD_FCCee_v01_fields": DetectorConfig(
        ddsim4FCC, ild4FCCDir / "ILD_FCCee_v01_fields/ILD_FCCee_v01_fields.xml"
    ),
    "ILD_FCCee_v01_fields_noMask": DetectorConfig(
        ddsim4FCC,
        ild4FCCDir / "ILD_FCCee_v01_fields_noMask/ILD_FCCee_v01_fields_noMask.xml",
    ),
    "ILD_FCCee_v02": DetectorConfig(
        ddsim4FCC, ild4FCCDir / "ILD_FCCee_v02/ILD_FCCee_v02.xml"
    ),
    "ILD_l5_v02": DetectorConfig(
        ddsim4ILC, ild4ILCDir / "ILD_l5_v02.xml"
    ),  # uniform solenoid field
    "ILD_l5_v03": DetectorConfig(
        ddsim4ILC, ild4ILCDir / "ILD_l5_v03.xml"
    ),  # realistic solenoid field
    "ILD_l5_v05": DetectorConfig(
        ddsim4ILC, ild4ILCDir / "ILD_l5_v05.xml"
    ),  # realistic solenoid field & anti-DID field
}


def replaceBXNumberInString(bsTypeName: str, bsPath: Path, bxN: int) -> str:
    if bsTypeName == "ILC250":
        return str(bsPath).replace("#N", str(bxN).zfill(4))
    return str(bsPath).replace("#N", str(bxN))


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
    for bs_scenario_name, bs_path_dict in bs_data_paths.items():
        if bs_scenario_name in acceleratorConfigs2Ana:
            for bunchCrossing in range(1, bunchCrossingEnd + 1):
                if checkMaxBXNumberExceeded(bs_scenario_name, bunchCrossing):
                    break

                bsPathWithBXNumber = replaceBXNumberInString(
                    bs_scenario_name,
                    get_path_for_current_machine(bs_path_dict),
                    bunchCrossing,
                )

                # Iterate over the detector models
                for detModName, detModConfigs in detectorConfigs.items():
                    if detModName in detMods2Ana:
                        # Construct the compactFile name
                        compactFile = k4geoDir / detModConfigs.relativeCompactFilePath

                        # Construct the output file names
                        outName = (
                            outDir
                            / f"{detModName}-{bs_scenario_name}-bX_{str(bunchCrossing).zfill(4)}-nEvts_{nEvents}"
                        )
                        outputFileName = outName.with_suffix(".edm4hep.root")
                        outputLogFileName = outName.with_suffix(".log")

                        # Construct the command
                        command = f"ddsim --steeringFile {detModConfigs.ddsimFile} --compactFile {compactFile} --inputFile {bsPathWithBXNumber} --outputFile {outputFileName} --numberOfEvents {nEvents} --guineapig.particlesPerEvent {guineaPigPartPerE} > {outputLogFileName} 2>&1"
                        bsub_command = f'bsub -q l "{command}"'

                        # Execute or print the command depending on executeBsub
                        if executeBsub:
                            subprocess.run(bsub_command, shell=True, check=True)
                        else:
                            print(bsub_command, end="\n\n")


if __name__ == "__main__":
    main()
