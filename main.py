"""
SIMON'S IMAGE COMPRESSOR
A command-line interface to compress images to .jpg format

Author: Simon Salvaing
Date: 2024-04-03

Entry point
"""
import sys

import typer

import config
import functions
import ui
import history

app = typer.Typer()


def main():
    """Main loop of the software"""
    ui.display_welcome_message()
    user_choice = 0
    while user_choice != len(config.OPTIONS):
        ui.display_menu()
        user_choice = ui.get_user_choice()
        config.OPTIONS[user_choice]["function"]()


@app.command()
def compress(quality: int = typer.Option(-1, help="Compression quality, from 1 (lower) to 95 (higher)")):
    """To compress 1 or more images to .jpg format."""

    path = functions.ask_for_image_or_folder_to_convert()
    if path is None:
        return

    destination_folder = functions.ask_for_destination_folder()
    if destination_folder is None:
        return

    quality = functions.ask_for_quality()

    files_to_convert = functions.get_files_to_convert(path=path)
    for each_file in files_to_convert:
        functions.compress(
            source_path=each_file,
            destination_folder=destination_folder,
            quality=quality
        )


@app.command('wtf')
def info():
    """To display information about the software."""
    ui.display_info_message()


@app.command('history')
def display_history():
    """To display your compression history."""
    history.display()


@app.command('search')
def search_in_history():
    """To search a string in filenames of your history."""
    history.search()


@app.command('clear')
def clear_history():
    """To clear your compression history."""
    history.clear()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        if sys.argv[-1] == "-h":
            sys.argv[-1] = "--help"
        app()
