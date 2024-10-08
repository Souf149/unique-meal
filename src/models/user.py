from enum import Enum
import datetime
import random
from datetime import date
from Crypto.Cipher import Salsa20
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import string


class Level:
    SUPER_ADMINISTRATOR = 1
    SYSTEM_ADMINISTRATORS = 2
    CONSULTANT = 3
    MEMBER = 4


def create_user_tuple(
    id: str,
    level: int,
    f_name: str,
    l_name: str,
    age: int,
    gender: str,
    weight: float,
    street: str,
    house_number: str,
    zip: str,
    city: str,
    email: str,
    phone: str,
    registration_date: date,
    username: str,
    hashed_pass: str,
) -> tuple:
    return (
        id,
        level,
        f_name,
        l_name,
        age,
        gender,
        weight,
        street,
        house_number,
        zip,
        city,
        email,
        phone,
        registration_date,
        username,
        hashed_pass,
    )


def create_user_dict(tup: tuple) -> dict:
    d: dict = {}

    d["id"] = tup[0]
    d["level"] = tup[1]
    d["f_name"] = tup[2]
    d["l_name"] = tup[3]
    d["age"] = tup[4]
    d["gender"] = tup[5]
    d["weight"] = tup[6]
    d["street"] = tup[7]
    d["house_number"] = tup[8]
    d["zip"] = tup[9]
    d["city"] = tup[10]
    d["email"] = tup[11]
    d["phone"] = tup[12]
    d["registration_date"] = tup[13]
    d["username"] = tup[14]
    d["hashed_pass"] = tup[15]

    return d


def generate_id():
    # First 2 digits
    year = str(datetime.date.today().year % 100)

    # Middle digits
    random_seq = []
    sum = int(year[0]) + int(year[1])
    for _ in range(7):
        rng = random.randint(1, 9)
        random_seq.append(str(rng))
        sum += rng

    # Adding the middle digits and adding the last 2
    result = year + "".join(random_seq) + str(sum % 10)
    return result


def hash_password(password: str) -> bytes:
    hash_object = SHA256.new(data=(password).encode())
    return hash_object.digest()


def generate_password():
    password = (
        random.choice(string.ascii_lowercase)
        + random.choice(string.ascii_uppercase)
        + random.choice(string.digits)
        + random.choice(string.punctuation)
    )
    for _ in range(10):
        password += random.choice(
            string.digits
            + string.ascii_lowercase
            + string.ascii_uppercase
            + string.punctuation
        )
    return password
