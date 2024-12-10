"""
contains detector model data:
    1. path to the model's compact file
    2. path to correct ddsim file
"""

from dataclasses import dataclass
from pathlib import Path

from g4units import rad

DEFAULT_DETECTOR_MODELS = "ILD_FCCee_v01", "ILD_l5_v02"


# Define the dataclass
@dataclass
class HitCollection:
    root_tree_branch_name: str
    plot_collection_prefix: str


@dataclass
class AcceleratorConfig:
    name: str
    relative_compact_file_dir: Path
    sim_crossing_angle_boost: float


@dataclass
class DetectorConfig:
    accelerator: AcceleratorConfig
    relative_compact_file_path: Path

    def get_compact_file_path(self) -> Path:
        # Combine the directory from the accelerator with the relative compact file path
        return (
            self.accelerator.relative_compact_file_dir / self.relative_compact_file_path
        )

    def get_crossing_angle(self) -> float:
        return self.accelerator.sim_crossing_angle_boost

    def is_accelerator_ilc(self) -> str:
        return self.accelerator.name == "ILC"

    def is_accelerator_fccee(self) -> str:
        return self.accelerator.name == "FCCee"


FCC_crossing_angle_boost = 15.0e-3
ILC_crossing_angle_boost = 7.0e-3
ild4FCC_dir = Path("FCCee") / "ILD_FCCee" / "compact"
ild4ILC_dir = Path("ILD") / "compact" / "ILD_sl5_v02"


accelerators = {
    "FCCee": AcceleratorConfig("FCCee", ild4FCC_dir, 15.0e-3 * rad),
    "ILC": AcceleratorConfig("ILC", ild4ILC_dir, 7.0e-3 * rad),
}


sub_detector_collections = {
    "vb": HitCollection(
        root_tree_branch_name="VertexBarrelCollection",
        plot_collection_prefix="Vertex Barrel",
    ),
    "ve": HitCollection(
        root_tree_branch_name="VertexEndcapCollection",
        plot_collection_prefix="Vertex Endcap",
    ),
}


detector_model_configurations = {
    "ILD_FCCee_v01": DetectorConfig(
        accelerators["FCCee"], "ILD_FCCee_v01/ILD_FCCee_v01.xml"
    ),
    "ILD_FCCee_v01_fields": DetectorConfig(
        accelerators["FCCee"], "ILD_FCCee_v01_fields/ILD_FCCee_v01_fields.xml"
    ),
    "ILD_FCCee_v01_fields_noMask": DetectorConfig(
        accelerators["FCCee"],
        "ILD_FCCee_v01_fields_noMask/ILD_FCCee_v01_fields_noMask.xml",
    ),
    "ILD_FCCee_v02": DetectorConfig(
        accelerators["FCCee"], "ILD_FCCee_v02/ILD_FCCee_v02.xml"
    ),
    "ILD_l5_v02": DetectorConfig(
        accelerators["ILC"], "ILD_l5_v02.xml"
    ),  # uniform solenoid field
    "ILD_l5_v03": DetectorConfig(
        accelerators["ILC"], "ILD_l5_v03.xml"
    ),  # realistic solenoid field
    "ILD_l5_v05": DetectorConfig(
        accelerators["ILC"], "ILD_l5_v05.xml"
    ),  # realistic solenoid field & anti-DID field
}

CHOICES_DETECTOR_MODELS = tuple(detector_model_configurations.keys())


def get_paths_and_detector_configs():
    return detector_model_configurations
