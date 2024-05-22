from abc import ABC, abstractmethod

from faker import Faker


class UserModel(ABC):
    FAKE = Faker()

    def __init__(self):
        self._user_type: str = ""
        self._email: str = ""
        self._password: str = ""
        self._first_name: str = ""
        self._last_name: str = ""
        self._addresses: list[dict] = []
        self._session: dict = {}

    # Getters & Setters
    @property
    def user_type(self) -> str:
        return self._user_type

    @user_type.setter
    def user_type(self, name: str) -> None:
        self._user_type = name

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        self._email = email

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = password

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        self._first_name = first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        self._last_name = last_name

    @property
    def addresses(self) -> list[dict]:
        return self._addresses

    @addresses.setter
    def addresses(self, addresses: list[dict]) -> None:
        self._addresses = addresses

    @property
    def session(self) -> dict:
        return self._session

    @session.setter
    def session(self, session: dict) -> None:
        self._session = session

    def get_password_positions(self, keyboard: [int]) -> [int]:
        """
              Get positions from android keyboard for digits in the password
                  :type keyboard: list[int]
                  :param keyboard: keyboard to evaluate and find positions
                  :return: list of positions of digits in the keyboard
              """
        password_digits = [int(char) for char in self.password if char.isdigit()]
        password_positions = []

        for digit in password_digits:
            if digit in keyboard:
                password_positions.append(keyboard.index(digit))

        return password_positions

    @abstractmethod
    def get_user(self) -> dict:
        return {
            self.user_type: {
                'email': self.email,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'addresses': self.addresses,
                'session': self.session
            }
        }

    @abstractmethod
    def find_category(self, category: str, categories: list[dict]) -> dict:
        raise NotImplementedError(f"Method not implemented {self.__class__.__name__}.find_category")

    def find_child_category(self, child_category: str, child_categories: list[dict]) -> None:
        raise NotImplementedError(f"Method not implemented {self.__class__.__name__}.find_child_category")

    @abstractmethod
    def clean(self) -> None:
        self.user_type = ""
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.addresses = [{}]
        self.session = {}
