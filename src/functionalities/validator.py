from datetime import date
import datetime
import re



class User_Info_Validator:
    def __init__(self, id: str, level: int, f_name: str, l_name: str, age: int, gender: str, 
                 weight: float, street: str, house_number: str, zip: str, city: str, 
                 email: str, phone: str, registration_date: date, username: str, 
                 hashed_pass: str):
        self.id = self.validate_id(id) #gedaan
        self.level = self.validate_level(level)
        self.f_name = self.validate_name(f_name) #gedaan
        self.l_name = self.validate_name(l_name) #gedaan
        self.age = self.validate_age(age)#gedaan
        self.gender = self.validate_gender(gender)
        self.weight = self.validate_weight(weight)#gedaan
        self.street = self.validate_name(street, "Street")
        self.house_number = self.validate_age(house_number, "House number")#straks kijken
        self.zip = self.validate_zip(zip, "Zip code")#gedaan
        self.city = self.validate_name(city, "City")#gedaan
        self.email = self.validate_email(email)#gedaan
        self.phone = self.validate_phone(phone)#gedaan
        self.registration_date = self.validate_registration_date(registration_date)#nog testen
        self.username = self.validate_username(username)#gedaan
        self.hashed_pass = self.validate_hashed_pass(hashed_pass)



    def validate_id(id) -> int:
        if isinstance(id, str):
            if not id.isdigit():
                return False
            id = int(id)

        if isinstance(id, int):
            if not 0 < id < 1000:
                return False
            return True
        
        return False


    def validate_password(password: str) -> bool:
        #  must have a length of at least 12 characters & ○	must have a length of at least 12 characters
        if len(password) < 12 or len(password) > 30:
            return False

        # 	must have a combination of at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False

        #  must have one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False

        # must have one digit
        if not re.search(r'[0-9]', password):
            return False

        # must have one special character
        if not re.search(r'[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/]', password):
            return False

        return True

    def validate_level(level: int) -> int:
        if isinstance(level, int) and 0 <= level <= 100:
            return level
        raise ValueError("Invalid level")

    def validate_name(self: str) -> bool:
            if not isinstance(self, str):
                return False
            # Removeleading/trailing spaces and check length
            self = self.strip()
            if 2 > len(self) > 50:
                return False          
            # Check if the name contains  digits
            if any(char.isdigit() for char in self):
                return False
            
            # Check if the first letter is uppercase (optional)
            if not (self[1:].islower()):
                return False
            
            if not re.match("^[A-Za-z]+$", self):  # No special characters
                return False
            return True  # If everything is valid, returns True

    def validate_age(age) -> bool:
        if not isinstance(age, (int, str)):  
            return False   
             
        if isinstance(age, str):  
            if not re.match("^[0-9]+$", age):  
                return False   
            try:
                age = int(age)
            except ValueError:
                return False   

        if 0 <= age <= 120:
            return True
        
        return False


    def validate_gender(gender: str) -> bool:
        if gender.upper() in {'M', 'F'}:
            return True
        return False
    
    def validate_weight(weight ) -> bool:
        if isinstance(weight, float) and 300 > weight > 0:
            return True

        if isinstance(weight, str):
            if re.match(r"^[0-9]*\.?[0-9]+$", weight): 
                weight = float(weight)  
                if 300 > weight > 0:
                    return True
        
        return False

    def validate_zip(field: str) -> str:
        if isinstance(field, str) and len(field) == 6 and re.match(r"^\d{4}[A-Za-z]{2}$", field):
            return True

        return False


    def validate_email(email: str) -> str:
        if not isinstance(email, str) or len(email) < 5 or len(email) > 254:
            return False

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if re.match(email_pattern, email):
            return True

        return False



    


    def validate_phone(phone: str) -> bool:

        phone = phone.strip()

        if phone.startswith('+'):
            if not phone[1:].isdigit():
                return False
            elif 15 >= (len(phone[1:])) >= 10:
                return True
        else:
            if not phone.isdigit():
                return False

        if 15 >= len(phone) >= 10:
            return True

        return False





    def validate_registration_date( registration_date) -> bool:
        if isinstance(registration_date, date):
            if registration_date > date.today():
                return False
            return True
        
        if isinstance(registration_date, str):
            try:
                parsed_date = datetime.strptime(registration_date, "%Y-%m-%d").date()

                if parsed_date > date.today():
                    return False

                return True
            except ValueError:
                return False
        
        return False



    def validate_username(username: str) -> bool:
        username = username.strip().lower()  # no distinguish between lowercase or uppercase letters

        # must be unique and have a length of at least 8 characters and max 10 characters
        if len(username) < 8 or len(username) > 10:
            return False

        # must be started with a letter or underscores (_)
        if not username[0].isalpha() and username[0] != '_':
            return False

        # 	can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)
        if not re.match("^[a-z0-9_.']+$", username):
            return False

        
        return True

    def validate_hashed_pass(self, hashed_pass: str) -> str:
        if isinstance(hashed_pass, str) and len(hashed_pass.strip()) > 0:
            return hashed_pass
        raise ValueError("Invalid password")

    def validate_housenumber(age) -> bool:
        if not isinstance(age, (int, str)): 
            return False   
             
        if isinstance(age, str):  
            if not re.match("^[0-9]+$", age):  
                return False   
            try:
                age = int(age)
            except ValueError:
                return False   

        if 0 <= age <= 9999:
            return True
        
        return False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "level": self.level,
            "f_name": self.f_name,
            "l_name": self.l_name,
            "age": self.age,
            "gender": self.gender,
            "weight": self.weight,
            "street": self.street,
            "house_number": self.house_number,
            "zip": self.zip,
            "city": self.city,
            "email": self.email,
            "phone": self.phone,
            "registration_date": self.registration_date,
            "username": self.username,
            "hashed_pass": self.hashed_pass
        }