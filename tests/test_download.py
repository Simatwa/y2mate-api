import unittest
from y2mate_api import Handler
from y2mate_api import main
from appdirs import AppDirs
import shutil
import os


appdir = AppDirs("y2mate_tests")

main.appdir = appdir

video_id = "jNQXAC9IVRw"


class TestDownload(unittest.TestCase):
    def setUp(self):
        self.handler = Handler(video_id)
        self.dir = "Downloads_test"
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

    def test_download_audio(self):
        """Downloads audio"""
        for audio_third_dict in self.handler.run("mp3", "128kbps"):
            audio_path = self.handler.save(
                audio_third_dict,
                self.dir,
                False,
                True,
            )
        self.assertIsInstance(audio_path, str)
        self.assertTrue(os.path.isfile(audio_path))
        """Affirms audio format"""
        self.assertIn("128", audio_path)
        self.assertIn(video_id, audio_path)
        self.assertTrue(audio_path.endswith("mp3"))

    def test_download_video(self):
        """Downloads video"""
        for video_third_dict in self.handler.run("mp4", "144p"):
            video_path = self.handler.save(video_third_dict, self.dir, False, True)
        self.assertIsInstance(video_path, str)
        self.assertTrue(os.path.isfile(video_path))
        """Affirms video format"""
        self.assertIn(video_id, video_path)
        self.assertIn("144", video_path)
        self.assertTrue(video_path.endswith("mp4"))

    def tearDown(self):
        shutil.rmtree(self.dir)


if __name__ == "__main__":
    unittest.main()
