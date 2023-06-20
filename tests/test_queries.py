import unittest
from y2mate_api import first_query, second_query, third_query


class test_first_query_using_title(unittest.TestCase):
    def setUp(self):
        self.first_query = first_query("hello world").main()

    def test_is_processed(self):
        self.assertTrue(self.first_query.processed)

    def test_status_is_ok(self):
        self.assertEqual(self.first_query.status, "ok")

    def test_is_not_link(self):
        self.assertFalse(self.first_query.is_link)

    def test_keyword_is_passed(self):
        self.assertEqual(self.first_query.keyword, "hello world")

    def test_has_list_vitems(self):
        self.assertIsInstance(self.first_query.vitems, list)

    def test_vitems_are_dict(self):
        self.assertIsInstance(self.first_query.vitems[0], dict)

    def test_raw_attribute_is_dict(self):
        self.assertIsInstance(self.first_query.raw, dict)


class test_second_query(unittest.TestCase):
    
    def setUp(self):
        self.video_id = "_z-1fTlSDF0"
        self.first_query = first_query(self.video_id).main()
        self.second_query = second_query(self.first_query).main()

    def test_query_is_processed(self):
        self.assertTrue(self.second_query.processed)

    def test_query_status_ok(self):
        self.assertEqual(self.second_query.status, "ok")

    def test_correct_video_id(self):
        self.assertEqual(self.second_query.vid, self.video_id)

    def test_video_extractor_is_youtube(self):
        self.assertTrue(self.second_query.extractor, "youtube")

    def test_video_author_is_infobells(self):
        self.assertTrue(self.second_query.a, "infobells")

    def test_has_attribute_audio(self):
        self.assertTrue(hasattr(self.second_query, "audio"))

    def test_attribute_video_is_dict(self):
        self.assertIsInstance(self.second_query.video, dict)

    def test_attribute_related_is_list(self):
        self.assertIs(type(self.second_query.related), list)

    def test_has_raw_attribute(self):
        self.assertTrue(hasattr(self.second_query, "raw"))


class test_third_query(unittest.TestCase):
    
    def setUp(self):
        self.video_id = "_z-1fTlSDF0"
        self.first_query = first_query(self.video_id).main()
        self.second_query = second_query(self.first_query).main()
        self.third_query = third_query(self.second_query).main()

    def test_response_is_dictionary(self):
        self.assertIs(type(self.third_query), dict)

    def test_confim_ok_status(self):
        self.assertEqual(self.third_query.get("status"), "ok")

    def test_video_is_processed(self):
        self.assertEqual(self.third_query.get("c_status"), "CONVERTED")

    def test_confirm_video_id(self):
        self.assertEqual(self.third_query.get("vid"), self.video_id)

    def test_confirm_video_title(self):
        self.assertEqual(self.third_query.get("title"), "Happy Birthday song")

    def test_affirm_video_ftype(self):
        self.assertEqual(self.third_query.get("ftype"), "mp4")

    def test_affirm_video_fquality(self):
        self.assertEqual(self.third_query.get("fquality"), "720p")

    def test_affirrm_video_link(self):
        self.assertIsNotNone(self.third_query.get("dlink"))


if __name__ == "__main__":
    unittest.main()
