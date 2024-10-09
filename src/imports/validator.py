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
    def validate_password(password: str) -> bool:  # Gecheckt op whitelisten
        if not "\x00" in password:
            if len(password) > 30:
                return False

            pattern = re.compile(
                r"^(?=.*[a-z])"
                r"(?=.*[A-Z])"
                r"(?=.*[0-9])"
                r"(?=.*[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/])"
                r".{12,30}$"
            )

            return bool(pattern.match(password))

        return False

    @staticmethod
    def validate_level(level: str | int) -> bool:  # Gecheckt op whitelisten
        max_length = 3

        if not "\0" in str(level):
            if isinstance(level, str) and len(level) > max_length:
                print(f"Input level exceeds maximum length of {max_length} characters.")
                return False

            return True

        print("Input level contains a null byte.")
        return False

    @staticmethod
    def validate_name(name: str) -> bool:  # Gecheckt op whitelisten
        if not "\x00" in name:
            if not isinstance(name, str):
                return False

            if not (2 <= len(name) <= 50):
                return False

            if not re.match("^[a-z]+$", name):
                return False

            return True

        return False

    @staticmethod
    def validate_street_name(street_name: str) -> bool:  # Gecheckt op whitelisten
        if not "\x00" in street_name:
            if not isinstance(street_name, str):
                return False

            MAX_INPUT_LENGTH = 1024
            if len(street_name) > MAX_INPUT_LENGTH:
                return False

            street_name = street_name.strip()

            if not (2 <= len(street_name) <= 100):
                return False

            if not re.match(r"^[A-Za-z .'-]+$", street_name):
                return False

            return True
        return False

    @staticmethod
    def validate_age(age) -> bool:  # Gecheckt op whitelisten
        valid_ages = set(range(0, 121))
        agebool = False
        if age is None:
            return False
        if "\0" not in age:
            if isinstance(age, str):
                if len(age) > 3:
                    return False
                if age.isdigit():
                    age = int(age)
                else:
                    return False
            agebool = age in valid_ages
        return agebool

    @staticmethod
    def validate_gender(gender: str) -> bool:  # Gecheckt op whitelisten
        if not "\x00" in gender:
            MAX_LENGTH = 1
            if len(gender) > MAX_LENGTH:
                return False

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
    def validate_zip(field: str) -> bool:  # Volledig gewhitelist
        if not "\x00" in field:
            if len(field) > 100:
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
    def validate_phone(phone: str) -> bool:  # volledig gewhitelist
        max_length = 8

        if not ("\0" in phone):
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

        return False

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
    def validate_username(username: str) -> bool:  # Gewcheckt op whitelist
        if not "\0" in username:
            username = username.strip().lower()

            MAX_LENGTH = 10

            # Allow only valid length (8 to MAX_LENGTH characters)
            if not (8 <= len(username) <= MAX_LENGTH):
                return False

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
    def validate_housenumber(
        housenumber, max_length=10
    ) -> bool:  # Gecheckt op whitelist
        if isinstance(housenumber, int):
            return 0 <= housenumber <= 9999

        if "\0" not in housenumber:
            if isinstance(housenumber, str):
                if len(housenumber) > max_length:
                    return False

                if re.match("^[0-9]+$", housenumber):
                    return 0 <= int(housenumber) <= 9999
            return False
        return False
