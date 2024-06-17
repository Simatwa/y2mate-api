import unittest
from y2mate_api import first_query, second_query, third_query


class test_first_query_using_title(unittest.TestCase):
    def setUp(self):
        self.first_query = first_query("hello world").main()

    def test_is_processed(self):
        """Tests first query is processed"""
        self.assertTrue(self.first_query.processed)

    def test_status_is_ok(self):
        """Tests status is ok"""
        self.assertEqual(self.first_query.status, "ok")

    def test_is_not_link(self):
        """Tests query param is not link"""
        self.assertFalse(self.first_query.is_link)

    def test_keyword_is_passed(self):
        """Tests keyword in response"""
        self.assertEqual(self.first_query.keyword, "hello world")

    def test_has_list_vitems(self):
        """Tests first_query has vitems"""
        self.assertIsInstance(self.first_query.vitems, list)

    def test_vitems_are_dict(self):
        """Tests vitems are in dictionary"""
        self.assertIsInstance(self.first_query.vitems[0], dict)

    def test_raw_attribute_is_dict(self):
        """Tests raw attribute is in dictionary"""
        self.assertIsInstance(self.first_query.raw, dict)


class test_first_query_using_link(unittest.TestCase):
    def setUp(self):
        self.video_id = "tPEE9ZwTmy0"
        self.url = "https://youtu.be/tPEE9ZwTmy0"
        self.first_query = first_query(self.url).main()

    def test_query_is_processed(self):
        """Tests first query is processed"""
        self.assertTrue(self.first_query.processed)

    def test_video_is_link(self):
        """Tests video is link"""
        self.assertTrue(self.first_query.is_link)

    def test_query_status_ok(self):
        """Tests status is processed"""
        self.assertEqual(self.first_query.status, "ok")

    def test_correct_video_id(self):
        """Tests video id"""
        self.assertEqual(self.first_query.vid, self.video_id)

    def test_video_extractor_is_youtube(self):
        """Tests video extractor"""
        self.assertTrue(self.first_query.extractor, "youtube")

    def test_video_author_is_Mylo_the_Cat(self):
        """Tests video author"""
        self.assertTrue(self.first_query.a, "Mylo the Cat")

    def test_video_title_is_correct(self):
        """Tests video title"""
        self.assertEqual(self.first_query.title, "Shortest Video on Youtube")

    def test_attribute_related_is_list(self):
        """Tests related is in list"""
        self.assertIs(type(self.first_query.related), list)

    def test_has_raw_attribute(self):
        """Tests raw attribute"""
        self.assertTrue(hasattr(self.first_query, "raw"))


class test_second_query(unittest.TestCase):
    def setUp(self):
        self.video_id = "_z-1fTlSDF0"
        self.first_query = first_query(self.video_id).main()
        self.second_query = second_query(self.first_query).main()

    def test_query_is_processed(self):
        """Test first query processed"""
        self.assertTrue(self.second_query.processed)

    def test_query_status_ok(self):
        """Tests query status"""
        self.assertEqual(self.second_query.status, "ok")

    def test_correct_video_id(self):
        """Tests video id"""
        self.assertEqual(self.second_query.vid, self.video_id)

    def test_video_extractor_is_youtube(self):
        """Tests video extractor"""
        self.assertTrue(self.second_query.extractor, "youtube")

    def test_video_author_is_infobells(self):
        """Tests video author"""
        self.assertTrue(self.second_query.a, "infobells")

    def test_has_attribute_audio(self):
        """Tests audio attribute"""
        self.assertTrue(hasattr(self.second_query, "audio"))

    def test_attribute_video_is_dict(self):
        """Tests video attribute"""
        self.assertIsInstance(self.second_query.video, dict)

    def test_attribute_related_is_list(self):
        """Tests related attribute"""
        self.assertIs(type(self.second_query.related), list)

    def test_has_raw_attribute(self):
        """Tests raw attribute"""
        self.assertTrue(hasattr(self.second_query, "raw"))


class test_third_query(unittest.TestCase):
    def setUp(self):
        self.video_id = "_z-1fTlSDF0"
        self.first_query = first_query(self.video_id).main()
        self.second_query = second_query(self.first_query).main()
        self.third_query = third_query(self.second_query).main()

    def test_response_is_dictionary(self):
        """Tests third_query response type"""
        self.assertIs(type(self.third_query), dict)

    def test_confim_ok_status(self):
        """Tests status code"""
        self.assertEqual(self.third_query.get("status"), "ok")

    def test_video_is_processed(self):
        """Tests video process state"""
        self.assertEqual(self.third_query.get("c_status"), "CONVERTED")

    def test_confirm_video_id(self):
        """Tests video id"""
        self.assertEqual(self.third_query.get("vid"), self.video_id)

    def test_confirm_video_title(self):
        """Tests video title"""
        self.assertEqual(self.third_query.get("title"), "Happy Birthday song")

    def test_Test_video_ftype(self):
        """Tests video ftype"""
        self.assertEqual(self.third_query.get("ftype"), "mp4")

    def test_Test_video_fquality(self):
        """Tests video fquality"""
        self.assertIn('720', self.third_query.get("fquality"))

    def test_affirrm_video_link(self):
        """Tests video link"""
        self.assertIsNotNone(self.third_query.get("dlink"))


if __name__ == "__main__":
    unittest.main()
