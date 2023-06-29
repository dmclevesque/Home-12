from collections import UserDict
from datetime import datetime, date

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        self._value = value

class Birthday(Field):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Birthday must be in format 'dd-mm-yyyy'")
        self._value = value

class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def add_birthday(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if not self.birthday:
            return
        current_date = date.today()
        birthday_date = datetime.strptime(self.birthday.value, "%d-%m-%Y").date().replace(year=current_date.year)
        if birthday_date < current_date:
            birthday_date = birthday_date.replace(year=current_date.year + 1)
        delta = birthday_date - current_date
        return delta.days

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i+n]

    def find(self, query):
        result = []
        for name, record in self.data.items():
            if query.lower() in name.lower():
                result.append(record)
                continue
            for phone in record.phones:
                if query in phone.value:
                    result.append(record)
                    break