import os
import tempfile
import unittest
from datetime import datetime, time, timezone

import database
from config import INDIA_TIMEZONE
from database import (
    get_emotion_entries,
    get_user_entry,
    register_user,
    save_entry,
    save_emotion_entry,
)
from utils import (
    filter_emotion_entries_by_period,
    filter_entries_by_period,
    get_intensity_band,
    get_today_date,
    to_india_datetime,
)


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
        occurred_at = datetime.now(INDIA_TIMEZONE).isoformat(timespec="seconds")

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

    def test_utc_timestamp_uses_india_calendar_date(self):
        india_today = datetime.now(INDIA_TIMEZONE).date()
        india_midnight = datetime.combine(india_today, time.min, tzinfo=INDIA_TIMEZONE)
        utc_timestamp = india_midnight.astimezone(timezone.utc).isoformat()
        entry = {
            "occurred_at": utc_timestamp,
            "emotion": "Fear",
            "intensity": 3,
            "cause": "",
        }

        self.assertEqual(get_today_date(), india_today.isoformat())
        self.assertEqual(to_india_datetime(utc_timestamp).date(), india_today)
        self.assertEqual(filter_emotion_entries_by_period([entry], "today"), [entry])
        habit_entry = (india_today.isoformat(), "{}")
        self.assertEqual(filter_entries_by_period([habit_entry], "today"), [habit_entry])

    def test_intensity_bands(self):
        self.assertEqual(get_intensity_band(2), ("🟢", "Gentle"))
        self.assertEqual(get_intensity_band(4), ("🟡", "Mild"))
        self.assertEqual(get_intensity_band(7), ("🟠", "Moderate"))
        self.assertEqual(get_intensity_band(8), ("🔴", "Strong"))

    def test_new_user_registration_is_stable_and_isolated(self):
        first_login = register_user("google-sub-1", "user@example.com", "New User")
        repeat_login = register_user("google-sub-1", "updated@example.com", "Updated Name")
        other_user = register_user("google-sub-2", "other@example.com", "Other User")

        self.assertEqual(first_login["username"], "google-sub-1")
        self.assertEqual(repeat_login["username"], first_login["username"])
        self.assertEqual(repeat_login["email"], "updated@example.com")
        self.assertNotEqual(other_user["username"], first_login["username"])

    def test_legacy_user_mapping_keeps_existing_entries(self):
        entry_date = "2026-11-05"
        self.assertTrue(save_entry("Bipin", entry_date, {"Yoga": True}))
        self.assertTrue(save_emotion_entry(
            "Bipin", "2026-11-05T10:00:00+05:30", "Happiness", 8, "Good news"
        ))

        user = register_user(
            "google-sub-bipin", "bipin@example.com", "Bipin", legacy_username="Bipin"
        )

        self.assertEqual(user["username"], "Bipin")
        self.assertEqual(get_user_entry(user["username"], entry_date)["habits"], {"Yoga": True})
        self.assertEqual(get_emotion_entries(user["username"])[0]["cause"], "Good news")


if __name__ == "__main__":
    unittest.main()
