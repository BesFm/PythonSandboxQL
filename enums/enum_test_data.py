from enum import Enum


class Handlers(Enum):
    base_url: str = "http://194.79.44.70:9090"
    get_bearer_token: str = "/api/v1/auth/login"
    get_users: str = "/api/v1/users_for_tests/"
    get_user_by_email: str = "/api/v1/users_for_tests/{user_by_email}"
    create_user: str = "/api/v1/users_for_tests/"


class UserDataLiza(Enum):
    first_name: str = "Elizaveta"
    last_name: str = "Podshivalova"
    email: str = "liz.podsh@mail.com"
    password: str = "qwerty"
    phone: str = "375294856935"


class UserDataMichal(Enum):
    first_name: str = "Michal"
    last_name: str = "Warsztat"
    email: str = "mih.warsztar@mail.ru"
    password: str = "qwertyqwertyqwertyqw"
    phone: str = "1234567891"
