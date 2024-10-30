import subprocess
from dataclasses import dataclass
from pathlib import Path
from os import getenv


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

# define dirs to detector models
codeDir = Path(getenv("myCodeDir"))
beamStrahlungCodeDir = codeDir / "beamStrahlung"
k4geoDir = codeDir / "k4geo"
ild4FCCDir = Path("FCCee") / "ILD_FCCee" / "compact"
ild4ILCDir = Path("ILD") / "compact" / "ILD_sl5_v02"
if "desy.de" in Path.home().parts:
    desyDustHomePath = Path("/nfs/dust/ilc/user/") / Path.home().parts[-1]
    outDir = desyDustHomePath
else:
    outDir = Path.home()
outDir = outDir / "promotion" / "data" / versionName

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

desyDustBeamstrahlungBasePath = desyDustHomePath / "beamStrahlungDataFromDaniel"
beamStrahlungDataPaths = {
    # are desy naf paths, the others are on the kek cc
    "ILC250": {
        "ilc": Path(
            "/group/ilc/users/jeans/pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.#N.pairs"
        ),
        "desy.de": desyDustBeamstrahlungBasePath
        / "pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.#N.pairs",
    },
    "FCC091": {
        "ilc": Path(
            "/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"
        ),
        "desy.de": desyDustBeamstrahlungBasePath
        / "tpc-ion_tpc-bspairs_input-allatip/pairs-#N_Z.pairs",
    },
    "FCC240": {
        "ilc": Path(
            "/home/ilc/jeans/guineaPig/fromAndrea/pairs100/allAtIP_ZH/pairs-#N_ZH.pairs"
        ),
        "desy.de": desyDustBeamstrahlungBasePath
        / "guineaPig_fromAndrea_pairs100_allAtIP-ZH/pairs-#N_ZH.pairs",
    },
}


def getPathForCurrentMachine(pathDict: dict) -> Path:
    pathParts = Path.home().parts
    for key in pathDict:
        if key in pathParts:
            return pathDict[key]
    raise KeyError(
        f"Machine unknown. One of the keys {list(pathDict)} has to be in {pathParts}."
    )


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
    for bsTypeName, bsPathDict in beamStrahlungDataPaths.items():
        if bsTypeName in acceleratorConfigs2Ana:
            for bunchCrossing in range(1, bunchCrossingEnd + 1):
                if checkMaxBXNumberExceeded(bsTypeName, bunchCrossing):
                    break

                bsPathWithBXNumber = replaceBXNumberInString(
                    bsTypeName, getPathForCurrentMachine(bsPathDict), bunchCrossing
                )

                # Iterate over the detector models
                for detModName, detModConfigs in detectorConfigs.items():
                    if detModName in detMods2Ana:
                        # Construct the compactFile name
                        compactFile = k4geoDir / detModConfigs.relativeCompactFilePath

                        # Construct the output file names
                        outName = (
                            outDir
                            / f"{detModName}-{bsTypeName}-bX_{str(bunchCrossing).zfill(4)}-nEvts_{nEvents}"
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
