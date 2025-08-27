import json
from tabulate import tabulate
import argparse
import os
from pathlib import Path
import pandas as pd
from get_hits_per_layer import divide_hits
from scale_hit_rate import scale_hits_dict

subdetector_labels = {
    "vb": "vertex barrel",
    "ve": "vertex endcap",
}

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Creates Table of hit rate for different detector models, scenarios and backgrounds"
    )
    parser.add_argument(
        "--version",
        "--directory",
        required=True,
        type=str,
        help="Version name / Directory containing the json_data directory; can be relative to the 'dtDir' env var",
    )
    parser.add_argument(
        "--unit",
        type=str,
        default="occupancy",
        choices=("per_bx", "per_bx_per_mm", "occupancy"),
        help="The units the values in the table will be given in. Occupancy values are given as percentages"
    )
    return parser.parse_args()

args = parse_arguments()

dt_dir = os.environ["dtDir"]  # Raises KeyError if not set — use .get() if you want a fallback

# Construct the json_dir path
json_dir = Path(dt_dir) / args.version / "json_data"

def extract_hits_per_bx(json_path):
    with open(json_path) as f:
        data = json.load(f)

    num_bx = data["num_bunch_crossings"]
    det_mod = data["detector_model"]
    scenario = data["scenario"]
    background = data["background"]
    hits = data["hits"]
    divided_hits = divide_hits(hits, det_mod)

    results_dict = scale_hits_dict(divided_hits, scenario, background, num_bx, det_mod)[args.unit]

    return det_mod, scenario, results_dict

def create_table():
    json_files = list(json_dir.glob("*.json"))

    rows = []

    for json_file in json_files:
        det_mod, scenario, hits = extract_hits_per_bx(json_file)
        for label, value in hits.items():
            formated_value = f" {value:.2e}"
            rows.append({
                "Detector Model": det_mod,
                "Subdetector": label,
                "Background": args.version,
                scenario: formated_value
            })

    # Create a DataFrame
    df = pd.DataFrame(rows)

    # Pivot so each scenario is a separate column
    df = df.pivot_table(
        index=["Detector Model", "Subdetector", "Background"],
        aggfunc="first"
    ).reset_index()

    # Sort the table for clarity
    df = df.sort_values(by=["Detector Model", "Subdetector", "Background"])

    if args.version == "synchrotron":
        first_three = df.columns[:3]  # keep first 3 as-is
        reorder_rest = ["45GeV_halo", "182GeV_halo", "182GeV_nzco_2urad",
                        "182GeV_nzco_6urad", "182GeV_nzco_10urad"]
        
        df = df[list(first_three) + reorder_rest]

    return df


def main():

    df = create_table()

    #print(tabulate(df, headers="keys", tablefmt="grid"))

    latex_table = tabulate(df, headers='keys', tablefmt='latex')
    with open(json_dir / "../background_table.tex", "w") as f:
        f.write(latex_table)
    markdown_table = tabulate(df, headers='keys', tablefmt='github')
    print(markdown_table)


if __name__ == "__main__":
    main()
