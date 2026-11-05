import base64
import hashlib
import hmac
import re
import secrets


PASSWORD_ITERATIONS = 600_000
PASSWORD_MIN_LENGTH = 12
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(email):
    normalized_email = (email or "").strip().lower()
    if not EMAIL_PATTERN.fullmatch(normalized_email):
        raise ValueError("Enter a valid email address")
    return normalized_email


def hash_password(password):
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters")

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS
    )
    salt_text = base64.urlsafe_b64encode(salt).decode("ascii")
    hash_text = base64.urlsafe_b64encode(password_hash).decode("ascii")
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt_text}${hash_text}"


def verify_password(password, encoded_hash):
    try:
        algorithm, iteration_text, salt_text, expected_hash_text = encoded_hash.split("$", 3)
        iterations = int(iteration_text)
        if algorithm != "pbkdf2_sha256" or not 100_000 <= iterations <= 2_000_000:
            return False
        salt = base64.urlsafe_b64decode(salt_text.encode("ascii"))
        expected_hash = base64.urlsafe_b64decode(expected_hash_text.encode("ascii"))
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations
        )
        return hmac.compare_digest(actual_hash, expected_hash)
    except (AttributeError, TypeError, ValueError):
        return False