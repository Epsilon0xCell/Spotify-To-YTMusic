#!/usr/bin/env python
"""Tests for reverse_playlist.py, the standalone backup file reverser."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from reverse_playlist import reverse_playlist


def write_file(directory, name, content):
    path = os.path.join(directory, name)
    with open(path, "w") as f:
        f.write(content)
    return path


PLAYLISTS = {
    "playlists": [
        {"name": "One", "tracks": [{"n": 1}, {"n": 2}, {"n": 3}]},
        {"name": "Two", "tracks": []},
    ]
}


class TestReversePlaylist(unittest.TestCase):
    def test_missing_file_returns_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, "nope.json")
            self.assertEqual(reverse_playlist(missing, verbose=False, replace=True), 1)

    def test_no_replace_flag_returns_1_and_leaves_file_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(tmp, "playlists.json", json.dumps(PLAYLISTS))
            self.assertEqual(reverse_playlist(path, verbose=False, replace=False), 1)
            with open(path) as f:
                self.assertEqual(json.load(f), PLAYLISTS)

    def test_replace_reverses_tracks_and_writes_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(tmp, "playlists.json", json.dumps(PLAYLISTS))
            self.assertEqual(reverse_playlist(path, verbose=False, replace=True), 0)
            with open(path) as f:
                result = json.load(f)
            self.assertEqual(
                [t["n"] for t in result["playlists"][0]["tracks"]], [3, 2, 1]
            )
            backup = os.path.join(tmp, "playlists_backup.json")
            self.assertTrue(os.path.exists(backup))
            with open(backup) as f:
                self.assertEqual(json.load(f), PLAYLISTS)

    def test_backup_lands_next_to_source_in_dotted_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            dotted = os.path.join(tmp, "sub.dir")
            os.mkdir(dotted)
            path = write_file(dotted, "data.json", json.dumps(PLAYLISTS))
            self.assertEqual(reverse_playlist(path, verbose=False, replace=True), 0)
            self.assertTrue(os.path.exists(os.path.join(dotted, "data_backup.json")))

    def test_invalid_json_returns_1_and_leaves_file_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(tmp, "playlists.json", "this is not json")
            self.assertEqual(reverse_playlist(path, verbose=False, replace=True), 1)
            with open(path) as f:
                self.assertEqual(f.read(), "this is not json")
            self.assertFalse(os.path.exists(os.path.join(tmp, "playlists_backup.json")))

    def test_missing_playlists_key_returns_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(tmp, "playlists.json", json.dumps({"foo": 1}))
            self.assertEqual(reverse_playlist(path, verbose=False, replace=True), 1)

    def test_playlist_without_tracks_returns_1_and_leaves_file_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = json.dumps({"playlists": [{"name": "Broken"}]})
            path = write_file(tmp, "playlists.json", content)
            self.assertEqual(reverse_playlist(path, verbose=False, replace=True), 1)
            with open(path) as f:
                self.assertEqual(f.read(), content)


if __name__ == "__main__":
    unittest.main()
