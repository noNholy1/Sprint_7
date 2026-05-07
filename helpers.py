from faker import Faker
import random

fake = Faker()
fakeRU = Faker(locale='ru_RU')


def create_random_login():
    return fake.user_name() + str(random.randint(0, 999))


def create_random_password():
    password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return password


def create_random_firstname():
    first_name = fakeRU.first_name()
    return first_name