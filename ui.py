from faker import Faker
import typer

import config

FAKE = Faker(locale="fr_FR")


def _display_line_separation(length: int):
    """Displays a line with random-colored stars"""
    characters = [typer.style('*', fg=FAKE.color_rgb()) for _ in range(length)]
    print("".join(characters))


def _display_starred_block(length: int):
    """Displays a random colored block of stars, nb_char long."""

    for _ in range(length):
        char = typer.style("*", fg=FAKE.color_rgb())
        print(char, end="")


def display_welcome_message():
    """Displays a welcome message"""

    line_length = 50
    _display_line_separation(line_length)
    # Pas besoin de faire une fonction pour ça, c'est juste un print et tu ne l'utilises qu'une fois.
    char = typer.style('*', fg=FAKE.color_rgb())
    print(char, "WELCOME TO SIMON'S IMAGE COMPRESSOR !".center(line_length - 2), char, sep='')
    _display_line_separation(line_length)


def display_menu():
    """Displays menu and returns user's choice as integer."""

    message = "What is your deepest wish ?"

    _display_line_separation(len(message))
    print(message, "\n")

    for i, option in config.OPTIONS.items():
        option_message = f"{i}: {option['display']}"
        print(typer.style(option_message, fg=FAKE.color_rgb()))


def get_user_choice() -> int:
    prompt = f"Choose a number from 1 to {len(config.OPTIONS)} then press Enter: "

    while True:
        user_input = input(f"👉🏼 {prompt}")
        if user_input.isdigit() and int(user_input) in config.OPTIONS:
            return int(user_input)
        else:
            print(f"Invalid input. Please enter a number between 1 and {len(config.OPTIONS)}.")


def display_goodbye_message():
    """Displays a goodbye message."""

    _display_starred_block(10)
    print(" Thanks, see you soon ! ", end="")
    _display_starred_block(10)
    print()


def display_info_message():
    """Displays a quick description of the software."""
    with open('README.md', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    for instruction in lines[:-1]:
        print(instruction)

    print("".join(typer.style(char, fg=FAKE.color_rgb()) for char in lines[-1]))


if __name__ == '__main__':
    choice = get_user_choice()
    print(choice)
