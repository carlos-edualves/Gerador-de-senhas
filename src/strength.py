import argparse
import secrets
import string

def evaluate_password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    
    has_lowercase = False
    has_uppercase = False
    has_number = False
    has_symbol = False

    for char in password:

        if char.islower():
            has_lowercase = True

        elif char.isupper():
            has_uppercase = True

        elif char.isdigit():
            has_number = True

        else:
            has_symbol = True

    if has_lowercase:
        score += 1

    if has_uppercase:
        score += 1

    if has_number:
        score += 1

    if has_symbol:
        score += 1

    return score

def get_password_strength(score):

    if score <= 1:
        return "Muito Fraca"

    elif score <= 3:
        return "Fraca"

    elif score <= 5:
        return "Média"

    elif score == 6:
        return "Forte"

    else:
        return "Muito Forte"