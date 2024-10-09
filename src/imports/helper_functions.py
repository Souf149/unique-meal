from datetime import date
import datetime
import random
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
import string
import os
import pyfiglet # type: ignore


class Level:
    SUPER_ADMINISTRATOR = 3
    SYSTEM_ADMINISTRATORS = 2
    CONSULTANT = 1


class PersonType:
    USER = "user"
    MEMBER = "member"


def clear_terminal_with_title(title="UNIQUE MEAL"):
    os.system(
        "cls" if os.name == "nt" else "clear"
    )  # Clear terminal for Windows or Unix
    big_title = pyfiglet.figlet_format(title, font="slant")  # Use a specific font
    print(big_title)  # Print the title


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


def hash_password(password: str) -> bytes:
    hash_object = SHA256.new(data=(password).encode())
    return hash_object.digest()


def user_input(prompt: str = "") -> str:
    res = ""
    while res == "":
        res = input(prompt + "\n")
    return str(res)


def create_member_tuple(
    id: str,
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
    hashed_pass: bytes,
) -> tuple:
    return (
        id,
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


def create_member_dict(tup: tuple) -> dict:
    d: dict = {}

    d["id"] = tup[0]
    d["f_name"] = tup[1]
    d["l_name"] = tup[2]
    d["age"] = tup[3]
    d["gender"] = tup[4]
    d["weight"] = tup[5]
    d["street"] = tup[6]
    d["house_number"] = tup[7]
    d["zip"] = tup[8]
    d["city"] = tup[9]
    d["email"] = tup[10]
    d["phone"] = tup[11]
    d["registration_date"] = tup[12]
    d["username"] = tup[13]
    d["hashed_pass"] = tup[14]

    d["type"] = PersonType.MEMBER

    return d


def create_user_dict(tup: tuple) -> dict:
    d: dict = {}

    d["id"] = tup[0]
    d["f_name"] = tup[1]
    d["l_name"] = tup[2]
    d["level"] = tup[3]
    d["username"] = tup[4]
    d["registration_date"] = tup[5]
    d["hashed_pass"] = tup[6]

    d["type"] = PersonType.USER

    return d


def create_user_tuple(
    id: str,
    f_name: str,
    l_name: str,
    level: int,
    username: str,
    registration_date: date,
    hashed_pass: bytes,
) -> tuple:
    return (
        id,
        f_name,
        l_name,
        level,
        username,
        registration_date,
        hashed_pass,
    )


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


def encrypt_tuple(
    tup: tuple[
        str,
        int,
        str,
        str,
        int,
        str,
        float,
        str,
        str,
        str,
        str,
        str,
        str,
        date,
        str,
        bytes,
    ],
) -> tuple:
    res: list[bytes] = []
    for val in tup:
        if isinstance(val, str):
            res.append(str.encode(val))
        elif isinstance(val, int):
            res.append(val.to_bytes(4, "big"))
        elif isinstance(val, float):
            res.append(val.hex().encode())
        elif isinstance(val, date):
            res.append(val.isoformat().encode())
        elif isinstance(val, bytes):
            res.append(val)
        else:
            raise Exception(
                f"Received a type I can not encrypt. value: {str(val)} of type: {type(val)}"
            )

    print(len(tup))
    print(len(res))
    fernet = Fernet("VyCIeFetb-w7Q3s_8xiuwHRDRLVSZI1sH13l3DJIS6w=")
    return tuple([fernet.encrypt(x) for x in res])


def decrypt_tuple(
    tup: tuple,
) -> tuple[
    str,
    int,
    str,
    str,
    int,
    str,
    float,
    str,
    str,
    str,
    str,
    str,
    str,
    date,
    str,
    bytes,
]:
    fernet = Fernet("VyCIeFetb-w7Q3s_8xiuwHRDRLVSZI1sH13l3DJIS6w=")
    decrypted_tup = [fernet.decrypt(x) for x in tup]

    float_str = bytes.decode(decrypted_tup[5])
    print(float_str)

    return create_member_tuple(
        bytes.decode(decrypted_tup[0]),
        bytes.decode(decrypted_tup[1]),
        bytes.decode(decrypted_tup[2]),
        int.from_bytes(decrypted_tup[3], "big"),
        bytes.decode(decrypted_tup[4]),
        float.fromhex(float_str),
        bytes.decode(decrypted_tup[6]),
        bytes.decode(decrypted_tup[7]),
        bytes.decode(decrypted_tup[8]),
        bytes.decode(decrypted_tup[9]),
        bytes.decode(decrypted_tup[10]),
        bytes.decode(decrypted_tup[11]),
        date.fromisoformat(bytes.decode(decrypted_tup[12])),
        bytes.decode(decrypted_tup[13]),
        decrypted_tup[14],
    )


if __name__ == "__main__":
    person = create_member_tuple(
        generate_id(),
        "Soufyan",
        "Abdell",
        25,
        "m",
        257.3,
        "otherstreet",
        "134",
        "2342",
        "Dordrecht",
        "0963595@hr.nl",
        "+31-6-21424244",
        date(2023, 3, 3),
        "souf149",
        hash_password("a"),
    )

    print(str(person) + "\n")

    e_person = encrypt_tuple(person)
    print(str(e_person) + "\n")

    print(str(decrypt_tuple(e_person)) + "\n")
