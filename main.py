"""
Модуль для зберігання та управління контактами у вигляді адресної книги.

Цей модуль надає класи для створення контактів, управління ними та зберігання
інформації в зручному форматі. Основні класи, які містяться в модулі, включають:

Класи:
--------
- Field: Базовий клас для всіх полів, що зберігають значення.
- Name: Клас для зберігання імені контакту, наслідує від Field.
- Phone: Клас для зберігання номера телефону, наслідує від Field. Обмежує номер
  телефону до останніх 10 символів.
- Record: Клас для зберігання контактної інформації, включаючи ім'я та список
  телефонів. Має методи для додавання, видалення, редагування та пошуку номерів.
- AddressBook: Клас для зберігання контактів у вигляді словника, де ключі — це імена,
  а значення — об'єкти Record.

Основні можливості:
-------------------
- Додавання та видалення контактів.
- Додавання, видалення, редагування телефонних номерів у контакті.
- Пошук контактів за ім'ям.
- Пошук телефонного номера всередині контакту.

Використання:
-------------
Адресна книга реалізована на основі UserDict, що дозволяє зручно працювати з контактами,
як зі звичайним словником. Модуль також обробляє помилки, такі як введення некоректних
номерів телефонів або редагування неіснуючого номера.
"""
from collections import UserDict
import re
from typing import Optional

class Field:
    """Базовий клас для всіх полів, що зберігають значення."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    """Клас для зберігання імені контакту, наслідує від Field."""

    def __init__(self, name: str) -> None:
        super().__init__(name)

class Phone(Field):
    """Клас для зберігання номера телефону, наслідує від Field.
    Номер телефону нормалізується та, якщо після нормалізації 
    він не пройшов перевірку, викликається виняток "ValueError".
    """

    def __init__(self, phone: str) -> None:
        phone = re.sub(r'\D', '', phone)
        if phone.startswith('38'):
            phone = phone[2:]
        if len(phone) != 10:
            raise ValueError(f"Phone number {phone} is invalid")
        super().__init__(phone)

class Record:
    """Клас для зберігання контактної інформації, включаючи ім'я та список телефонів."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Додає новий номер телефону до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видаляє номер телефону із запису, якщо він існує."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Редагує існуючий номер телефону на новий. 
        Викликає ValueError, якщо старий номер не знайдено."""
        for p in self.phones:
            if p.value == old_phone:
                p = Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Шукає і повертає об'єкт Phone, якщо він існує, або None, якщо не знайдено."""
        return next((p for p in self.phones if p.value == phone), None)

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    """Клас для зберігання контактів у вигляді словника, 
    де ключі — це імена, а значення — об'єкти Record."""

    def add_record(self, record: Record) -> None:
        """Додає новий запис Record до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Шукає запис Record за ім'ям. Повертає Record або None, якщо запис не знайдено."""
        return self.data.get(name, None)

    def delete(self, name: str) -> None:
        """Видаляє запис Record за ім'ям, якщо він існує в адресній книзі."""
        self.data.pop(name, None)

    def __str__(self) -> str:
        """Повертає текстове представлення всіх записів у адресній книзі."""
        return '\n'.join(str(record) for record in self.data.values())

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("+38123456-7890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")

print(book)
