#!/usr/bin/env python3

import json
import os
import shutil
import sys
from argparse import ArgumentParser


def reverse_playlist(input_file="playlists.json", verbose=True, replace=False) -> int:
    # I check for the file first. This used to go straight to the backup
    # copy, and a missing input file died inside shutil.copyfile with a
    # FileNotFoundError traceback instead of one plain error line.
    if not os.path.exists(input_file):
        print(f"ERROR: Input file not found: {input_file}")
        return 1

    # The output of this script is the input file itself, rewritten. So
    # this refusal is not really about a second file existing. It is a
    # guard on the -r flag: if I did not pass -r, I have not said out loud
    # that I accept overwriting the only copy I am standing on, backup
    # or not, and the script stops.
    if not replace:
        if verbose:
            print(
                "Output file already exists and no replace argument detected, exiting..."
            )
        return 1

    print("Backing up file...")
    # splitext, not split("."). Splitting on every dot turned
    # ./playlists.json into a backup named _backup.json in the current
    # directory and cut a path like sub.dir/data.json off at the
    # directory name. The backup has to land next to its source, under a
    # name I can find again, because it is the only way back if the
    # reversal below writes a bad file.
    backup_file = os.path.splitext(input_file)[0] + "_backup.json"
    shutil.copyfile(input_file, backup_file)
    # Load the JSON file
    with open(input_file, "r") as file:
        if verbose:
            print("Loading initial JSON file...")
        data = json.load(file)

    # Copy the data to a new dictionary
    # This copy is shallow and I know it: the playlist dicts inside are
    # shared with data, and the reversal below replaces their tracks
    # lists in place. That is fine here because nothing after this point
    # reads the original order from memory. The original order survives
    # in the backup file on disk, not in this process.
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
    # Verbose defaults to on and -v used to be store_false, which meant
    # passing the flag that claimed to enable verbose actually silenced
    # the script. Now -v and --no-verbose write the same dest from two
    # sides, so the flag I pass says what it does.
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

    # sys.exit around the call matters. This used to call the function
    # and throw its return value away, so the refusal above exited 0 and
    # any script wrapping this one read a stopped run as a success.
    sys.exit(reverse_playlist(args.input_file, args.verbose, args.replace))
