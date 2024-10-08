import re
from typing import Any

from tools.tools import check_password


def is_valid(key: str, value: Any):
    try:
        if key == "age":
            return str(int(value)).isdigit()

        if key == "gender":
            return value in ["m", "f"]

        if key == "weight":
            float(value)
            return True

        if key == "email":
            return bool(
                re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(
                    value
                )
            )

        if key == "phone":
            return bool(re.compile(r"^\d{8}$").match(value))

        if key == "password":
            return check_password(value)

        return True

    except:
        return False
