import os
import tempfile
import unittest
from datetime import datetime

import database
from utils import filter_emotion_entries_by_period


class EmotionTrackingTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = database.LOCAL_DB_PATH
        self.original_use_local_db = database.USE_LOCAL_DB
        database.LOCAL_DB_PATH = os.path.join(self.temp_dir.name, "test.db")
        database.USE_LOCAL_DB = True
        database.init_db()

    def tearDown(self):
        database.LOCAL_DB_PATH = self.original_db_path
        database.USE_LOCAL_DB = self.original_use_local_db
        self.temp_dir.cleanup()

    def test_saves_and_filters_emotion_occurrences(self):
        occurred_at = datetime.now().astimezone().isoformat(timespec="seconds")

        self.assertTrue(database.save_emotion_entry(
            "Test User", occurred_at, "Nervousness", 7, "Before a presentation"
        ))
        self.assertTrue(database.save_emotion_entry(
            "Test User", occurred_at, "Happiness", 4, "Good news"
        ))

        entries = database.get_emotion_entries("Test User")
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["cause"], "Good news")
        self.assertEqual(entries[1]["intensity"], 7)
        self.assertEqual(len(filter_emotion_entries_by_period(entries, "today")), 2)
        self.assertEqual(database.get_emotion_entries("Another User"), [])


if __name__ == "__main__":
    unittest.main()
