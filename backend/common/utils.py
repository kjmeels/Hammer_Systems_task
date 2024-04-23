import random
from time import sleep
import string


def generate_4_symbols_code():
    return random.randint(1000, 10000)


def send_code():
    sleep(2)
    return None


def get_invite_code():
    letters = list(string.ascii_uppercase)
    digits = list(string.digits)
    characters = letters + digits
    return "".join(random.sample(characters, 6))
