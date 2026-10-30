#!/usr/bin/env python

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from spotify2ytmusic import backend


def make_fixture():
    """Return a temp playlists file based on tests/playliststest.json, extended
    with a "Liked Songs" playlist and a liked album, which the shipped fixture
    does not contain."""
    with open("tests/playliststest.json") as f:
        data = json.load(f)

    def track(name, artist, album):
        return {
            "track": {
                "name": name,
                "artists": [{"name": artist}],
                "album": {"name": album},
            }
        }

    data["playlists"].append(
        {
            "name": "Liked Songs",
            "id": "liked_songs_test",
            "tracks": [track("Liked One", "Artist One", "Album One"),
                       track("Liked Two", "Artist Two", "Album Two")],
        }
    )
    data["albums"] = [
        {
            "album": {
                "name": "Album One",
                "tracks": {
                    "items": [
                        {"name": "Album Track", "artists": [{"name": "Artist One"}]}
                    ]
                },
            }
        }
    ]

    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
    return path


def make_mock_yt():
    """A YTMusic stand-in whose searches always find one song."""
    instance = MagicMock()
    instance.get_playlist.return_value = {"title": "Test Playlist"}
    instance.add_playlist_items.return_value = None
    song = {
        "title": "Found Song",
        "artists": [{"name": "Found Artist"}],
        "album": {"name": "Found Album"},
        "videoId": "found_video_id",
    }

    def search(query, filter=None):
        if filter == "albums":
            return []
        return [song]

    instance.search.side_effect = search
    instance.get_album.return_value = {"tracks": []}
    return instance


class TestCopier(unittest.TestCase):
    def setUp(self):
        self.fixture = make_fixture()
        self.mock_yt = make_mock_yt()
        patcher = patch.object(
            backend, "get_ytmusic", return_value=self.mock_yt
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(os.unlink, self.fixture)

    def test_copier_success(self):
        backend.copier(
            backend.iter_spotify_playlist(
                "68QlHDwCiXfhodLpS72iOx",
                spotify_playlist_file=self.fixture,
            ),
            dst_pl_id="dst_test",
            track_sleep=0,
        )

        self.mock_yt.get_playlist.assert_called_once_with(playlistId="dst_test")
        self.assertTrue(self.mock_yt.add_playlist_items.called)

    def test_copier_albums(self):
        backend.copier(
            backend.iter_spotify_liked_albums(
                spotify_playlist_file=self.fixture
            ),
            dst_pl_id="dst_test",
            track_sleep=0,
        )

        self.mock_yt.get_playlist.assert_called_once_with(playlistId="dst_test")
        self.assertTrue(self.mock_yt.add_playlist_items.called)

    def test_copier_liked_playlists(self):
        backend.copier(
            backend.iter_spotify_playlist(
                None, spotify_playlist_file=self.fixture
            ),
            dst_pl_id="dst_test",
            track_sleep=0,
        )

        self.mock_yt.get_playlist.assert_called_once_with(playlistId="dst_test")
        self.assertTrue(self.mock_yt.add_playlist_items.called)

    def test_copier_skips_track_that_is_not_found(self):
        # Regression test: lookup_song raises ValueError for a track that
        # cannot be found (search algos 1 and 2). The copier must give up on
        # that track after a few retries instead of retrying it forever.
        tracks = iter([backend.SongInfo("Missing", "Nobody", "Nowhere")])
        with patch.object(
            backend,
            "lookup_song",
            side_effect=ValueError("Did not find Missing by Nobody from Nowhere"),
        ), patch.object(backend.time, "sleep", return_value=None):
            backend.copier(tracks, dst_pl_id="dst_test", track_sleep=0)

        self.assertFalse(self.mock_yt.add_playlist_items.called)


if __name__ == "__main__":
    unittest.main()
