"""Main functions and constants"""
import typer
from PIL import Image
from faker import Faker
from tinydb import TinyDB, Query

from pathlib import Path
from datetime import datetime


def welcome():
    """Displays a welcome message"""
    line_length = 50

    def title():
        """Displays centered title, between random-colored stars"""
        char = typer.style('*', fg=FAKE.color_rgb())
        print(char, "WELCOME TO SIMON'S IMAGE COMPRESSOR !".center(line_length - 2), char, sep='')

    starred_line(line_length)
    title()
    starred_line(line_length)


def starred_line(length: int):
    """Displays a line with random-colored stars"""
    for _ in range(length):
        char = typer.style('*', fg=FAKE.color_rgb())
        print(char, end='')
    print()


def display_menu() -> int:
    """Displays menu and returns user's choice as integer."""

    message_1 = "What is your deepest wish ?"
    message_2 = f"Select a number from 1 to {len(OPTIONS)} then press Enter: "

    print()
    starred_line(len(message_1))
    print(message_1, "\n")
    for i, option in OPTIONS.items():
        line = typer.style(f"{i}: {option['display']}", fg=FAKE.color_rgb())
        print(line)

    valid = False
    user_choice = ""
    while not valid:
        user_choice = input(f"👉🏼 {message_2}")
        try:
            user_choice = int(user_choice)
        except ValueError:
            print(f"Invalid input. {message_2}")
            print()
        else:
            if user_choice in OPTIONS:
                valid = True
            else:
                print(f"This number is not an option! {message_2}")
                print()
    return user_choice


def ask_for_path() -> Path | str:
    """Asks the user for the image(s) file or folder path, check if this
    path exists, then if yes returns it as Path object
    (or returns the string 'Q' if user wants to exit).
    """
    print("What is the path of the image(s) file or folder (or 'Q' to exit): ",
          end="")

    while True:
        path = input()
        if path.upper() == 'Q':
            return 'Q'

        path = Path(path)
        if not path.exists():
            print("This path doesn't exist, or is not recognized.")
            print("Try again (or 'Q' to exit): ", end="")
            continue

        return path


def check_destination_folder(folder: Path) -> Path | str:
    """
    Checks if folder exists. If not, asks user to give a valid folder path.
    Returns valid folder path (original or given by user).
    """
    valid_path = ""
    if folder.exists():
        valid_path = folder
    else:
        while not valid_path:
            user_path = Path(input("Specify the destination folder (or 'Q' to exit): "))
            if user_path.exists() and user_path.is_dir():
                valid_path = user_path
            elif str(user_path).upper() == 'Q':
                valid_path = 'Q'
            elif user_path.is_file():
                print("This is a file path, not a folder path... 😵‍💫")
            else:
                print("This path doesn't exist, or is not recognized... 😰")
    return valid_path


# Functions called from the menu
def info():
    """Displays a quick description of the software."""
    with open('what_is_it.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            print(line, end='')
        else:
            for char in line:
                char = typer.style(char, fg=FAKE.color_rgb())
                print(char, end='')
    print()


def compress(quality: int = -1):
    """
    To compress 1 or more files to .jpg format.
    Quality is defaulted to -1 in parameters so that function can recognize if this option was
    specified in command line. Default value will be changed to 75 if not.
    """

    def check_duplicate_names(src_path: Path) -> Path | None:
        """
        Check if there is already a file with the same name and extension in
        the destination folder. If yes, suffixes the output file name with a
        number (ex: image - 001.jpg).
        Returns the output file path.
        """
        dest_path = destination_folder / (src_path.stem + '.jpg')
        new_path = dest_path
        i = 0
        while new_path in destination_folder.glob("*.jpg"):
            i += 1
            new_path = dest_path.with_stem(
                dest_path.stem + f" - {str(i).zfill(3)}")
        return new_path

    def choose_quality(quality_level: int) -> int | str:
        """
        If quality is not specified in command line, asks user
        the compression quality level desired.
        Returns it, or 75 if user just presses Enter.
        """
        if quality_level == -1:
            quality_level = 75
            print("Compression quality is defaulted to 75, "
                  "in a scale from 1 (lower) to 95 (higher).")
            valid_input = False
            while not valid_input:
                user_quality = input("Press enter if 75 is OK, or specify "
                                     "a number between 1 and 95: ")
                if not user_quality:
                    valid_input = True
                else:
                    try:
                        user_quality = int(user_quality)
                    except ValueError:
                        print("Not a number! ", end="")
                        continue
                    else:
                        if user_quality not in range(1, 96):
                            print("Invalid choice. ", end="")
                            continue
                        else:
                            quality_level = user_quality
                            valid_input = True
        return quality_level

    def compression(src_path: Path, dest_path: Path):
        """
        Compress an image to destination folder, or displays an error message
        if source file is not an image file.
        """
        try:
            im = Image.open(src_path)
            im.save(dest_path, "JPEG", optimize=True, quality=quality)
        except OSError as e:
            print(typer.style(f"Problem with the '{src_path.name}' file: {e}",
                              fg=typer.colors.RED))
        else:
            print(typer.style(f"Compression of '{src_path.name}' completed in the "
                  f"'{destination_folder}' folder (quality: {quality}).", fg=typer.colors.GREEN))
            DB.insert({"date": str(datetime.now()), "filename": src_path.name})

    source_path = ask_for_path()
    if source_path == 'Q':
        return
    destination_folder = check_destination_folder(Path.home() / "Downloads1")
    if destination_folder == 'Q':
        return

    quality = choose_quality(quality)
    if source_path.is_file():
        new_im_path = check_duplicate_names(source_path)
        compression(source_path, new_im_path)
    elif source_path.is_dir():
        for file in source_path.glob("*.*"):
            new_im_path = check_duplicate_names(file)
            compression(file, new_im_path)


def search_in_history():
    """
    Asks users for a string to search in filenames contained in the history,
    then displays results.
    """
    if DB.all():
        compression = Query()
        user_request = input(
            "What do you want to search in the filenames contained in the history ? "
        )
        results = DB.search(compression.filename.search(user_request))
        if results:
            print("Here's the list of all matching files in the history:")
            for entry in results:
                print(f"{entry['date']}: "
                      f"{typer.style(entry['filename'], fg=typer.colors.YELLOW)}")
        else:
            print(f"No match with '{user_request}' found in the filenames.")
    else:
        print("Nothing to search, your history is empty ! 😯")


def display_history():
    """
    Displays the entire history.
    """
    if DB.all():
        print("Here's the list of all successful compressions "
              "realized since last clearing:")
        for entry in iter(DB):
            print(f"{entry['date']}: "
                  f"{typer.style(entry['filename'], fg=FAKE.color_rgb())}")
    else:
        print("Your history is empty. 😯")


def clear_history():
    """Clears the history"""
    if DB.all():
        message = "Are you sure you want to clear your compression history ? [y/N] "
        user_choice = input(message)
        if user_choice.upper() == 'Y':
            DB.truncate()
            print("Your history is cleared.")
    else:
        print("Nothing to clear! Your history is empty.")


def goodbye():
    """Displays a goodbye message."""

    def starred_block(length: int):
        """Displays a random colored block of stars, nb_char long."""
        for _ in range(length):
            char = typer.style("*", fg=FAKE.color_rgb())
            print(char, end="")

    starred_block(10)
    print(" Thanks, see you soon ! ", end="")
    starred_block(10)
    print()


FAKE = Faker(locale="fr_FR")
DB = TinyDB("history.json", indent=4, encoding='utf-8')
OPTIONS = {
        1: {"display": "Know more about this software",
            "function": info},
        2: {"display": "Compress image(s)", "function": compress},
        3: {"display": "Search in the history", "function": search_in_history},
        4: {"display": "Display the history", "function": display_history},
        5: {"display": "Clear the history", "function": clear_history},
        6: {"display": "Quit", "function": goodbye},
    }


if __name__ == '__main__':
    pass
