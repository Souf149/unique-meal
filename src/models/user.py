from enum import Enum
import datetime
import random
from datetime import date
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import string


class Level(Enum):
    SUPER_ADMINISTRATOR = 1
    SYSTEM_ADMINISTRATORS = 2
    CONSULTANT = 3
    MEMBER = 4


def create_user(id: str, level: int, f_name: str, l_name: str, age: int, gender: str, weight: float, street: str, house_number: str, zip: str, city: str, email: str, phone: str, registration_date: date, username: str, hashed_pass: str) -> dict:
    d: dict = {}

    d["id"] = id
    d["level"] = level
    d["f_name"] = f_name
    d["l_name"] = l_name
    d["age"] = age
    d["gender"] = gender
    d["weight"] = weight
    d["street"] = street
    d["house_number"] = house_number
    d["zip"] = zip
    d["city"] = city
    d["email"] = email
    d["phone"] = phone
    d["registration_date"] = registration_date
    d["username"] = username
    d["hashed_pass"] = hashed_pass

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
    password = random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase) + \
        random.choice(string.digits) + random.choice(string.punctuation)
    for _ in range(10):
        password += random.choice(string.digits + string.ascii_lowercase +
                                  string.ascii_uppercase + string.punctuation)
    return password
