import unittest

from src.validator import (
    validate_email,
    validate_phone,
    InvalidEmailError,
    InvalidPhoneError,
)


class TestValidator(unittest.TestCase):

    # --- Email Tests ---
    def test_valid_emails(self):
        """Valid emails should return True."""
        valid_cases = [
            "user@example.com",
            "first.last@company.org",
            "test+tag@domain.co.uk",
        ]
        for email in valid_cases:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))

    def test_invalid_emails(self):
        """Invalid emails should raise InvalidEmailError."""
        invalid_cases = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user@domain",
            "",
            "   ",
            None,
        ]
        for email in invalid_cases:
            with self.subTest(email=email):
                with self.assertRaises(InvalidEmailError):
                    validate_email(email)

    # --- Phone Tests ---
    def test_valid_phones(self):
        """Valid Turkish phone numbers in different formats should return True."""
        valid_cases = [
            "05551112233",
            "5551112233",
            "+90 555 111 22 33",
            "(0555) 111-22-33",
            "905551112233",
        ]
        for phone in valid_cases:
            with self.subTest(phone=phone):
                self.assertTrue(validate_phone(phone))

    def test_invalid_phones(self):
        """Invalid phone number formats should raise InvalidPhoneError."""
        invalid_cases = [
            "12345",  # Too short
            "02121234567",  # Landline prefix (does not start with 5)
            "0555111223344",  # Too long
            "no_phone",  # Non-numeric string
            "",  # Empty string
            "   ",  # Whitespace only
            None,  # NoneType
        ]
        for phone in invalid_cases:
            with self.subTest(phone=phone):
                with self.assertRaises(InvalidPhoneError):
                    validate_phone(phone)


if __name__ == "__main__":
    unittest.main()
