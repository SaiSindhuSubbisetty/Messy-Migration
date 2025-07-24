# utils/validators.py
import re

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$"

def is_valid_email(email: str) -> bool:
    return bool(re.match(EMAIL_REGEX, email))

def is_strong_password(password: str) -> bool:
    return bool(re.match(PASSWORD_REGEX, password))
