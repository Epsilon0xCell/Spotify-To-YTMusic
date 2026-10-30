#!/usr/bin/env python3

import json
import os
import shutil
import sys
from argparse import ArgumentParser


def reverse_playlist(input_file="playlists.json", verbose=True, replace=False) -> int:
    if not os.path.exists(input_file):
        print(f"ERROR: Input file not found: {input_file}")
        return 1

    if not replace:
        if verbose:
            print(
                "Output file already exists and no replace argument detected, exiting..."
            )
        return 1

    print("Backing up file...")
    backup_file = os.path.splitext(input_file)[0] + "_backup.json"
    shutil.copyfile(input_file, backup_file)
    # Load the JSON file
    with open(input_file, "r") as file:
        if verbose:
            print("Loading initial JSON file...")
        data = json.load(file)

    # Copy the data to a new dictionary
    data2 = data.copy()

    if verbose:
        print("Reversing playlists...")
    # Reverse the order of items in the "tracks" list
    for i in range(len(data2["playlists"])):
        # Reverse the tracks in the playlist
        data2["playlists"][i]["tracks"] = data2["playlists"][i]["tracks"][::-1]

    if verbose:
        print("Writing to file... (this can take a while)")
    # Write the modified JSON back to the file
    with open(input_file, "w") as file:
        json.dump(data2, file)

    if verbose:
        print("Done!")
        print(f"File can be found at {input_file}")

    return 0


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=True,
        help="Print progress messages (on by default; use --no-verbose to silence)",
    )
    parser.add_argument(
        "--no-verbose",
        dest="verbose",
        action="store_false",
        help="Silence progress messages",
    )
    parser.add_argument(
        "-r",
        "--replace",
        action="store_true",
        help="Replace the output file if already existing",
    )

    args = parser.parse_args()

    sys.exit(reverse_playlist(args.input_file, args.verbose, args.replace))
