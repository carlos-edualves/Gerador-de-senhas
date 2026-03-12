import argparse
import secrets
import string


def generate_password(length, use_numbers, use_symbols, use_uppercase, use_lowercase):

    characters = ""
    score = 0

    if use_lowercase:
        characters += string.ascii_lowercase

    if use_uppercase:
        characters += string.ascii_uppercase

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("Você precisa selecionar pelo menos uma opção!")

    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password