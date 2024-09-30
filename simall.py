import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DetectorConfig:
    ddsimFile: Path
    relativeCompactFilePath: Path


# Define the variables
bunchCrossingEnd = 2
nEvents = 5000
guineaPigPartPerE = -1
versionName = "python_test"
detMods2Ana = {"ILD_FCCee_v01", "ILD_FCCee_v02"}
acceleratorConfigs2Ana = {"FCC91", "FCC240"}
executeBsub = False  # Boolean variable to switch between modes


outDir = Path.home() / "promotion" / "data" / versionName
# define dirs to detector models
k4geoDir = Path.home() / "promotion" / "code" / "k4geo"
ild4FCCDir = Path("FCCee") / "ILD_FCCee" / "compact"

# define Paths to ddsim files
ddsim4FCCee = Path.home() / "promotion/code/bs/ddsim_keep_microcurlers_10MeV_30mrad.py"

# Source the setup script (this will be a no-op in Python, since sourcing doesn't propagate in subprocess)
setupScriptPath = "/cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh"

# Dict containing the detector model configurations
detectorConfigs = {
    "ILD_FCCee_v01": DetectorConfig(
        ddsim4FCCee, ild4FCCDir / "ILD_FCCee_v01/ILD_FCCee_v01.xml"
    ),
    "ILD_FCCee_v02": DetectorConfig(
        ddsim4FCCee, ild4FCCDir / "ILD_FCCee_v02/ILD_FCCee_v02.xml"
    ),
    "ILD_FCCee_v01_fields": DetectorConfig(ddsim4FCCee, ild4FCCDir),
    "ILD_FCCee_v01_fields_noMask": DetectorConfig(ddsim4FCCee, ild4FCCDir),
}

beamStrahlungDataPaths = {
    "ILC250": Path(
        "/group/ilc/users/jeans/pairs-ILC250_gt2MeV/E250-SetA.PBeamstr-pairs.GGuineaPig-v1-4-4-gt2MeV.I270000.#N.pairs"
    ),
    "FCC91": Path("/home/ilc/jeans/tpc-ion/tpc-bspairs/input_allatip/pairs-#N_Z.pairs"),
    "FCC240": Path(
        "/home/ilc/jeans/guineaPig/fromAndrea/pairs100/allAtIP_ZH/pairs-#N_ZH.pairs"
    ),
}


def replaceBXNumberInString(bsTypeName, bsPath, bxN):
    if bsTypeName == "ILC250":
        return str(bsPath).replace("#N", str(bxN).zfill(4))
    return str(bsPath).replace("#N", str(bxN))


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
    for bsTypeName, bsPath in beamStrahlungDataPaths.items():
        if bsTypeName in acceleratorConfigs2Ana:

            for bunchCrossing in range(1, bunchCrossingEnd + 1):

                bsPathWithBXNumber = replaceBXNumberInString(
                    bsTypeName, bsPath, bunchCrossing
                )

                # Iterate over the detector models
                for detModName, detModConfigs in detectorConfigs.items():
                    if detModName in detMods2Ana:

                        ddsimFile = detModConfigs.ddsimFile

                        # Construct the compactFile Name
                        compactFile = k4geoDir / detModConfigs.relativeCompactFilePath

                        # Construct the output file name
                        outName = (
                            outDir
                            / f"{detModName}-{bsTypeName}-bX_{str(bunchCrossing).zfill(4)}-nEvts_{nEvents}"
                        )
                        outputFileName = outName.with_suffix(".edm4hep.root")
                        outputLogFileName = outName.with_suffix(".log")

                        # Construct the command
                        command = f"ddsim --steeringFile {ddsimFile} --compactFile {compactFile} --inputFile {bsPathWithBXNumber} --outputFile {outputFileName} --numberOfEvents {nEvents} --guineapig.particlesPerEvent {guineaPigPartPerE} > {outputLogFileName} 2>&1"
                        bsub_command = f'bsub -q l "{command}"'

                        # Execute or print the command depending on execute_bsub
                        if executeBsub:
                            subprocess.run(bsub_command, shell=True)
                        else:
                            print(bsub_command, end="\n\n")


if __name__ == "__main__":
    main()
