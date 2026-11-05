import os
import tempfile
import unittest

import database
from auth import hash_password, normalize_email, verify_password
from database import get_password_user, get_user_entry, register_password_user, save_entry


class PasswordAuthTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = database.LOCAL_DB_PATH
        self.original_use_local_db = database.USE_LOCAL_DB
        database.LOCAL_DB_PATH = os.path.join(self.temp_dir.name, "accounts.db")
        database.USE_LOCAL_DB = True
        database.init_db()

    def tearDown(self):
        database.LOCAL_DB_PATH = self.original_db_path
        database.USE_LOCAL_DB = self.original_use_local_db
        self.temp_dir.cleanup()

    def test_password_hash_is_salted_and_verified(self):
        first_hash = hash_password("a-long-test-password")
        second_hash = hash_password("a-long-test-password")

        self.assertNotEqual(first_hash, second_hash)
        self.assertTrue(verify_password("a-long-test-password", first_hash))
        self.assertFalse(verify_password("incorrect-password", first_hash))
        self.assertFalse(verify_password("anything", "invalid-hash"))
        with self.assertRaises(ValueError):
            hash_password("short")

    def test_signup_signin_email_normalization_and_data_isolation(self):
        account = register_password_user(
            "User@Example.com", "Test User", hash_password("a-long-test-password")
        )
        other_account = register_password_user(
            "other@example.com", "Other User", hash_password("another-long-password")
        )
        signed_in_account = get_password_user(" USER@example.com ")

        self.assertEqual(signed_in_account["id"], account["id"])
        self.assertTrue(verify_password("a-long-test-password", signed_in_account["password_hash"]))
        self.assertNotEqual(account["username"], other_account["username"])
        self.assertTrue(save_entry(account["username"], "2026-11-05", {"Yoga": True}))
        self.assertIsNone(get_user_entry(other_account["username"], "2026-11-05"))
        with self.assertRaises(ValueError):
            register_password_user("user@example.com", "Duplicate", hash_password("a-long-test-password"))

    def test_email_validation(self):
        self.assertEqual(normalize_email(" User@Example.com "), "user@example.com")
        with self.assertRaises(ValueError):
            normalize_email("not-an-email")


if __name__ == "__main__":
    unittest.main()