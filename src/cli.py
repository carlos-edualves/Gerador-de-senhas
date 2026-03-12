import argparse

from src.generator import generate_password
from src.strength import evaluate_password_strength, get_password_strength

def run_cli():

    parser = argparse.ArgumentParser(description="Secure Password Generator")

    parser.add_argument("--length", type=int, default=12, help="Password length")
    parser.add_argument("--numbers", action="store_true", help="Include numbers")
    parser.add_argument("--symbols", action="store_true", help="Include symbols")
    parser.add_argument("--uppercase", action="store_true", help="Include uppercase letters")
    parser.add_argument("--lowercase", action="store_true", help="Include lowercase letters")

    args = parser.parse_args()

    try:
        password = generate_password(
            args.length,
            args.numbers,
            args.symbols,
            args.uppercase,
            args.lowercase
        )
        score = evaluate_password_strength(password)
        strength = get_password_strength(score)
        print(f"\nGenerated password: {password}\n")
        print(f"Strong Level: {strength}\n")

    except ValueError as e:
        print(f"Error: {e}")