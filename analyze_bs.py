import argparse
from os import fspath
from pathlib import Path

from podio import root_io

inputFileDefault = (
    Path.home()
    / "promotion/data/TEST_IMPROVED/ILD_FCCee_v01/pairs-2_ZHatIP_tpcTimeKeepMC_keep_microcurlers_10MeV_30mrad_ILD_FCCee_v01.emd4hep.root"
    # / "promotion/data/TEST_IMPROVED/ILD_FCCee_v01/pairs-1_ZHatIP_tpcTimeKeepMC_keep_microcurlers_10MeV_30mrad_ILD_FCCee_v01.slcio"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputFile",
        "-f",
        default=fspath(inputFileDefault),
        type=str,
        help="relative path to the input file",
    )

    args = parser.parse_args()
    inputFile = args.inputFile

    reader = root_io.Reader(fspath(inputFile))
    events = reader.get("events")

    for e in events:
        vertex_barrel_collection = e.get("VertexBarrelCollection")
        vertex_endcap_collection = e.get("VertexEndcapCollection")
        for vertex_barrel_hit, vertex_endcap_hit in zip(
            vertex_barrel_collection, vertex_endcap_collection
        ):
            print(vertex_barrel_hit.getPosition().x)
            print(vertex_barrel_hit.getPosition().y)
            print(vertex_barrel_hit.getPosition().z)
            print(vertex_barrel_hit.getTime())
            print(vertex_endcap_hit.getPosition().x)
            print(vertex_endcap_hit.getPosition().y)
            print(vertex_endcap_hit.getPosition().z)
            print(vertex_endcap_hit.getTime())

    # tmrrw
    # import awkward as ak

    # Create empty lists to store the data
    # barrel_positions_x = []
    # barrel_positions_y = []
    # barrel_positions_z = []
    # barrel_times = []

    # endcap_positions_x = []
    # endcap_positions_y = []
    # endcap_positions_z = []
    # endcap_times = []

    # Loop through the events and store the data
    # for e in events:
    #     vertex_barrel_collection = e.get("VertexBarrelCollection")
    #     vertex_endcap_collection = e.get("VertexEndcapCollection")

    #     barrel_x = []
    #     barrel_y = []
    #     barrel_z = []
    #     barrel_time = []

    #     endcap_x = []
    #     endcap_y = []
    #     endcap_z = []
    #     endcap_time = []

    #     for vertex_barrel_hit, vertex_endcap_hit in zip(vertex_barrel_collection, vertex_endcap_collection):
    #         barrel_x.append(vertex_barrel_hit.getPosition().x)
    #         barrel_y.append(vertex_barrel_hit.getPosition().y)
    #         barrel_z.append(vertex_barrel_hit.getPosition().z)
    #         barrel_time.append(vertex_barrel_hit.getTime())

    #         endcap_x.append(vertex_endcap_hit.getPosition().x)
    #         endcap_y.append(vertex_endcap_hit.getPosition().y)
    #         endcap_z.append(vertex_endcap_hit.getPosition().z)
    #         endcap_time.append(vertex_endcap_hit.getTime())

    #     # Store the per-event data into the main lists
    #     barrel_positions_x.append(barrel_x)
    #     barrel_positions_y.append(barrel_y)
    #     barrel_positions_z.append(barrel_z)
    #     barrel_times.append(barrel_time)

    #     endcap_positions_x.append(endcap_x)
    #     endcap_positions_y.append(endcap_y)
    #     endcap_positions_z.append(endcap_z)
    #     endcap_times.append(endcap_time)

    # # Convert the lists into awkward arrays
    # barrel_positions_x = ak.Array(barrel_positions_x)
    # barrel_positions_y = ak.Array(barrel_positions_y)
    # barrel_positions_z = ak.Array(barrel_positions_z)
    # barrel_times = ak.Array(barrel_times)

    # endcap_positions_x = ak.Array(endcap_positions_x)
    # endcap_positions_y = ak.Array(endcap_positions_y)
    # endcap_positions_z = ak.Array(endcap_positions_z)
    # endcap_times = ak.Array(endcap_times)

    # experimenting
    e = reader.get("events")[0]
    vertex_barrel_collection = e.get("VertexBarrelCollection")
    vertex_endcap_collection = e.get("VertexEndcapCollection")

    print(vertex_barrel_collection[0].getPosition().x)
    print(vertex_endcap_collection[0].getTime())

    import time

    from IPython import embed

    embed()
    time.sleep(1)


main()
