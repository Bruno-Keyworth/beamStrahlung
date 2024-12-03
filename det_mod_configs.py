"""
contains detector model data:
    1. path to the model's compact file
    2. path to correct ddsim file
"""

from dataclasses import dataclass
from pathlib import Path

CHOICES_DETECTOR_MODELS = tuple(
    {
        "ILD_FCCee_v01",
        "ILD_FCCee_v01_fields",
        "ILD_FCCee_v02",
        "ILD_l5_v02",
        "ILD_l5_v03",
        "ILD_l5_v05",
    }
)
DEFAULT_DETECTOR_MODELS = "ILD_FCCee_v01", "ILD_l5_v02"


@dataclass
class DetectorConfig:
    ddsim_file: Path
    relative_compact_file_path: Path


def get_paths_and_detector_configs(bs_code_dir: Path):
    ild4FCC_dir = Path("FCCee") / "ILD_FCCee" / "compact"
    ild4ILC_dir = Path("ILD") / "compact" / "ILD_sl5_v02"
    ddsim4FCC = bs_code_dir / "ddsim_keep_microcurlers_10MeV_30mrad.py"
    ddsim4ILC = bs_code_dir / "ddsim_keep_microcurlers_10MeV.py"

    det_mod_configs_dir_internal = {
        "ILD_FCCee_v01": DetectorConfig(
            ddsim4FCC, ild4FCC_dir / "ILD_FCCee_v01/ILD_FCCee_v01.xml"
        ),
        "ILD_FCCee_v01_fields": DetectorConfig(
            ddsim4FCC, ild4FCC_dir / "ILD_FCCee_v01_fields/ILD_FCCee_v01_fields.xml"
        ),
        "ILD_FCCee_v01_fields_noMask": DetectorConfig(
            ddsim4FCC,
            ild4FCC_dir / "ILD_FCCee_v01_fields_noMask/ILD_FCCee_v01_fields_noMask.xml",
        ),
        "ILD_FCCee_v02": DetectorConfig(
            ddsim4FCC, ild4FCC_dir / "ILD_FCCee_v02/ILD_FCCee_v02.xml"
        ),
        "ILD_l5_v02": DetectorConfig(
            ddsim4ILC, ild4ILC_dir / "ILD_l5_v02.xml"
        ),  # uniform solenoid field
        "ILD_l5_v03": DetectorConfig(
            ddsim4ILC, ild4ILC_dir / "ILD_l5_v03.xml"
        ),  # realistic solenoid field
        "ILD_l5_v05": DetectorConfig(
            ddsim4ILC, ild4ILC_dir / "ILD_l5_v05.xml"
        ),  # realistic solenoid field & anti-DID field
    }

    return det_mod_configs_dir_internal
