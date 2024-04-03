"""
SIMON'S IMAGE COMPRESSOR
A command-line interface to compress images to .jpg format

Author: Simon Salvaing
Date: 2024-04-03

Entry point
"""
import sys

import typer

import functions as f

app = typer.Typer()


def main():
    """Main loop of the software"""
    f.welcome()
    user_choice = 0
    while user_choice != len(f.OPTIONS):
        user_choice = f.display_menu()
        print()
        f.OPTIONS[user_choice]["function"]()


@app.command()
def compress(quality: int = typer.Option(-1,
             help="Compression quality, from 1 (lower) to 95 (higher)")):
    """
    To compress 1 or more images to .jpg format.
    """
    f.compress(quality=quality)


@app.command('wtf')
def info():
    """To display information about the software."""
    f.info()


@app.command('history')
def display_history():
    """To display your compression history."""
    f.display_history()


@app.command('search')
def search_in_history():
    """To search a string in filenames of your history."""
    f.search_in_history()


@app.command('clear')
def clear_history():
    """To clear your compression history."""
    f.clear_history()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        if sys.argv[-1] == "-h":
            sys.argv[-1] = "--help"
        app()
