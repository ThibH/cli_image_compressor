"""Main functions"""
import typer
from PIL import Image

from pathlib import Path
from datetime import datetime

import config
import database


def ask_for_image_or_folder_to_convert() -> Path | None:
    """Asks the user for the image(s) file or folder path, check if this
    path exists, then if yes returns it as Path object
    (or returns None if user wants to exit).
    """
    print("What is the path of the image(s) file or folder (or 'Q' to exit): ",
          end="")

    while True:
        path = input()
        if path.upper() == 'Q':
            return None

        path = Path(path)
        if not path.exists():
            print("This path doesn't exist, or is not recognized.")
            print("Try again (or 'Q' to exit): ", end="")
            continue

        return path


def ask_for_destination_folder() -> Path | None:
    """Asks user to give a valid folder path.
    Returns valid folder path (original or given by user) or None if user wants to exit.
    """
    valid_path = ""
    while not valid_path:
        user_path = Path(input("Specify the destination folder (or 'Q' to exit): "))
        if user_path.is_dir():
            valid_path = user_path
        elif str(user_path).upper() == 'Q':
            valid_path = 'Q'
        elif user_path.is_file():
            print("This is a file path, not a folder path... 😵‍💫")
        else:
            print("This path doesn't exist, or is not recognized... 😰")
    return valid_path


def ask_for_quality() -> int:
    """Asks the user for the compression quality level."""
    while True:
        user_input = input("Press enter if 75 is OK, or specify a number between 1 and 95: ")
        if not user_input:  # Si l'utilisateur appuie simplement sur Entrée.
            return config.DEFAULT_QUALITY
        try:
            quality = int(user_input)
            if 1 <= quality <= 95:
                return quality
            else:
                print("Invalid choice. Please specify a number between 1 and 95: ", end="")
        except ValueError:
            print("Not a number! Please specify a valid number: ", end="")


def _get_unique_file_path(folder_path_destination: Path, file_path_source: Path) -> Path | None:
    """
    Check if there is already a file with the same name and extension in
    the destination folder. If yes, suffixes the output file name with a
    number (ex: image - 001.jpg).
    Returns the output file path.
    """
    dest_path = folder_path_destination / f'{file_path_source.stem}.jpg'
    new_path = dest_path
    i = 0
    while new_path in folder_path_destination.glob("*.jpg"):
        i += 1
        new_path = dest_path.with_stem(f"{dest_path.stem} - {str(i).zfill(3)}")
    return new_path


def _compression(source: Path, target: Path, quality: int):
    """Compress an image to destination folder, or displays an error message
    if source file is not an image file."""
    try:
        im = Image.open(source)
        im.save(target, "JPEG", optimize=True, quality=quality)
    except OSError as e:
        print(typer.style(f"Problem with the '{source.name}' file: {e}",
                          fg=typer.colors.RED))
    else:
        print(typer.style(f"Compression of '{source.name}' completed in the "
                          f"'{target}' folder (quality: {quality}).", fg=typer.colors.GREEN))
        database.DB.insert({"date": str(datetime.now()), "filename": source.name})


def get_files_to_convert(path: Path) -> list[Path]:
    """Get all files to convert : if path given is a file, return it, otherwise, get all files inside folder."""

    return [path] if path.is_file() else list(path.glob("*.*"))


def compress(source_path: Path, destination_folder: Path, quality: int = None):
    """
    To compress 1 or more files to .jpg format.
    Quality is defaulted to -1 in parameters so that function can recognize if this option was
    specified in command line. Default value will be changed to 75 if not.
    """

    if not quality or quality == -1:
        quality = config.DEFAULT_QUALITY

    unique_file_path = _get_unique_file_path(file_path_source=source_path, folder_path_destination=destination_folder)
    _compression(source=source_path, target=unique_file_path, quality=quality)
