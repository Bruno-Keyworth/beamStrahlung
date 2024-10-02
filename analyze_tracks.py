import argparse
from os import fspath
from pathlib import Path

import matplotlib.pyplot as plt
from podio import root_io

input_file_path = (
    Path.home()
    / "promotion/code/ILDConfig/StandardConfig/production/data/muon_tracking_test_if1_REC.edm4hep.root"
)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process and display track hit data.")
    parser.add_argument(
        "--mode",
        choices=["print", "plot"],
        required=True,
        help="Choose 'print' to display hit numbers, or 'plot' to show histograms.",
    )

    args = parser.parse_args()

    f = root_io.Reader(fspath(input_file_path))

    # Get the list of events and determine the number of events
    events = f.get("events")
    total_events = len(events)

    # Print the total number of available events
    print(f"Total number of available events: {total_events}")

    # List of collections we're interested in
    collections_of_interest = ["SiTracksCT", "ClupatraTracks"]

    # Dictionary to store hit counts per collection
    hit_counts = {collection: [] for collection in collections_of_interest}

    # Flag to control printing
    should_print_hits = args.mode == "print"

    # Iterate over each event in the file
    for event_index, e in enumerate(events, start=1):
        if should_print_hits:
            # Format the event number with leading zeros
            event_number = f"{event_index:03d}"
            print(f"Event {event_number}:")

        # Loop over each collection of interest
        for collection_name in collections_of_interest:
            try:
                first_track = e.get(collection_name)[0]
                n_tracker_hits = first_track.trackerHits_size()

                # Append hit count to the respective list in the dictionary
                hit_counts[collection_name].append(n_tracker_hits)

                # Print hits if mode is 'print'
                if should_print_hits:
                    print(
                        f"  {n_tracker_hits} hits were found for the {collection_name}"
                    )

            except IndexError:
                # Handle the case where the collection might be empty
                if should_print_hits:
                    print(f"  No tracks available in the {collection_name}")
                hit_counts[collection_name].append(0)

    # Plot histograms if mode is 'plot'
    if args.mode == "plot":
        for collection_name, counts in hit_counts.items():
            plt.figure()
            plt.hist(counts, bins=range(max(counts) + 2), alpha=0.75)
            plt.title(f"Histogram of Hit Counts for {collection_name}")
            plt.xlabel("Number of Hits")
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.show()


if __name__ == "__main__":
    main()
