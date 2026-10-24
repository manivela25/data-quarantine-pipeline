import re


class ValidationError(Exception):
    "validation errors"
    pass


class InvalidEmailError(ValidationError):
    "invalid email format"
    pass


class InvalidPhoneError(ValidationError):
    "invalid phone number format"
    pass


def validate_email(email):
    if not isinstance(email, str) or not email.strip():
        raise InvalidEmailError("Email address cannot be empty.")

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email.strip()):
        raise InvalidEmailError(f"Invalid email format: {email}")

    return True


def validate_phone(phone):
    if not isinstance(phone, str) or not phone.strip():
        raise InvalidPhoneError("Phone number cannot be empty.")

    cleaned = re.sub(r"\D", "", phone)

    if cleaned.startswith("90") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    elif cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = cleaned[1:]

    if len(cleaned) != 10 or not cleaned.startswith("5"):
        raise InvalidPhoneError(f"Invalid phone number: {phone}")

    return True
