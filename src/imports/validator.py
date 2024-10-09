from datetime import date
import datetime
import re


class User_Info_Validator:
    @staticmethod
    def validate_id(membershipid: str) -> bool:
        digits = [int(digit) for digit in membershipid[:-1]]
        digit_sum = sum(digits)
        expected_checksum = digit_sum % 10
        actual_checksum = int(membershipid[-1])

        return actual_checksum == expected_checksum

    @staticmethod
    def validate_password(password: str) -> bool:
        if "\x00" in password:  # null-bytes check
            return False

        # Check for maximum length
        if len(password) > 30:
            return False

        # regex pattern with specifically whitelisting
        pattern = re.compile(
            r"^(?=.*[a-z])"  # At least one lowercase letter
            r"(?=.*[A-Z])"  # At least one uppercase letter
            r"(?=.*[0-9])"  # At least one digit
            r"(?=.*[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/])"  # At least one special character
            r".{12,30}$"  # Length between 12 and 30 characters
        )

        # Match the password against the compiled pattern
        return bool(pattern.match(password))

    @staticmethod
    def validate_level(level: str | int) -> bool:
        # Buffer overflow check: limit input length
        max_length = 3  # Assuming level should be a maximum of 3 digits (to accommodate levels up to 999)
        if isinstance(level, str) and len(level) > max_length:
            print(f"Input level exceeds maximum length of {max_length} characters.")
            return False

        # Null-byte check
        if "\0" in str(level):
            print("Input level contains a null byte.")
            return False

        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        if not isinstance(name, str):
            return False

        name = name.strip()

        if not (2 <= len(name) <= 50):
            return False

        if "\x00" in name:
            return False

        if not re.match("^[a-z]*$", name):  # First letter uppercase, rest lowercase
            return False

        return True

    @staticmethod
    def validate_street_name(street_name: str) -> bool:
        if not isinstance(street_name, str):
            return False

        MAX_INPUT_LENGTH = 1024
        if len(street_name) > MAX_INPUT_LENGTH:
            return False

        street_name = street_name.strip()

        if not (2 <= len(street_name) <= 100):
            return False

        if "\x00" in street_name:
            return False

        if not re.match(r"^[A-Za-z .'-]+$", street_name):
            return False

        return True

    @staticmethod
    def validate_age(age) -> bool:
        valid_ages = set(range(0, 121))

        if age is None:
            return False

        if isinstance(age, str):
            if "\0" in age:  # Check for null bytes
                return False  # Reject input with null bytes
            if len(age) > 3:
                return False
            if age.isdigit():  # Check if it's a numeric string
                age = int(age)
            else:
                return False  # Reject non-numeric strings

        return age in valid_ages

    @staticmethod
    def validate_gender(gender: str) -> bool:
        # Check for null bytes
        if "\x00" in gender:
            return False

        MAX_LENGTH = 1
        if len(gender) > MAX_LENGTH:
            return False

        # Validate against whitelisted values
        if gender.upper() in {"M", "F"}:
            return True

        return False

    @staticmethod
    def validate_weight(weight) -> bool:
        # Check for null bytes in string representation
        if isinstance(weight, str):
            if (
                "\0" in weight or len(weight) > 20
            ):  # Limit string length to 20 characters
                return False

        # Validate numeric types
        if isinstance(weight, (int, float)) and 0 < weight < 300:
            return True

        if isinstance(weight, str):
            # Match valid integers or floats, with an optional decimal point
            if re.fullmatch(r"\d+(\.\d+)?", weight):
                weight = float(weight)
                if 0 < weight < 300:
                    return True

        return False

    @staticmethod
    def validate_zip(field: str) -> bool:
        # Check for null bytes
        if "\x00" in field:
            return False

        # Check for excessively long input (beyond expected size)
        if len(field) > 100:  # Set an arbitrary limit, e.g., 100 characters
            return False

        if (
            isinstance(field, str)
            and len(field) == 6
            and re.match(r"^\d{4}[A-Za-z]{2}$", field)
        ):
            return True

        return False

    @staticmethod
    def validate_email(email: str) -> bool:
        MAX_EMAIL_LENGTH = 254

        if (
            not isinstance(email, str)
            or len(email) < 5
            or len(email) > MAX_EMAIL_LENGTH
            or "\0" in email
        ):
            return False

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        return bool(re.match(email_pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        max_length = 8

        # Check for null bytes in the input
        if "\0" in phone:
            return False

        if len(phone) > max_length:
            return False

        phone = phone.strip()

        valid_length = 8
        valid_characters = set("0123456789")

        if len(phone) != valid_length:
            return False

        for char in phone:
            if char not in valid_characters:
                return False

        return True

    @staticmethod
    def validate_registration_date(registration_date) -> bool:
        MAX_STRING_LENGTH = 10  # "YYYY-MM-DD" is 10 characters

        if isinstance(registration_date, date):
            return registration_date <= date.today()

        if isinstance(registration_date, str):
            # Check for null bytes in the string
            if "\x00" in registration_date:
                return False

            # Check for excessive length
            if len(registration_date) > MAX_STRING_LENGTH:
                return False

            try:
                parsed_date = datetime.datetime.strptime(
                    registration_date, "%Y-%m-%d"
                ).date()
                return parsed_date <= date.today()
            except ValueError:
                return False

        return False

    @staticmethod
    def validate_username(username: str) -> bool:
        # Check for null bytes
        if "\0" in username:
            return False

        username = (
            username.strip().lower()
        )  # Normalize the username to lowercase and strip whitespace

        # Maximum length for usernames to prevent buffer overflows
        MAX_LENGTH = 10

        # Allow only valid length (8 to MAX_LENGTH characters)
        if not (8 <= len(username) <= MAX_LENGTH):
            return False

        # Whitelist criteria:
        # 1. Must start with a letter (a-z) or an underscore (_)
        if username[0].isalpha() or username[0] == "_":
            # 2. Must contain only allowed characters: letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)
            if re.match("^[a-z0-9_.']+$", username):
                return True

        return False

    @staticmethod
    def validate_hashed_pass(hashed_pass: str) -> str:
        if isinstance(hashed_pass, str) and len(hashed_pass.strip()) > 0:
            return hashed_pass
        raise ValueError("Invalid password")

    @staticmethod
    def validate_housenumber(housenumber, max_length=10) -> bool:
        if isinstance(housenumber, int):
            return 0 <= housenumber <= 9999

        if isinstance(housenumber, str):
            # Whitelist: Must not contain null bytes
            if "\0" in housenumber:
                return False

            if len(housenumber) > max_length:
                return False

            if re.match("^[0-9]+$", housenumber):
                return 0 <= int(housenumber) <= 9999

        return False
