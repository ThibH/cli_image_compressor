import typer
from faker import Faker

import database
from tinydb import Query

FAKE = Faker(locale="fr_FR")


def check_empty_db(func):
    def wrapper(*args, **kwargs):
        if not database.DB.all():  # Vérifie si la base de données est vide
            print("Your history is empty. 😯")
            return  # Sortie anticipée de la fonction
        return func(*args, **kwargs)  # Exécute la fonction originale si la DB n'est pas vide

    return wrapper


@check_empty_db
def search():
    """
    Asks users for a string to search in filenames contained in the history,
    then displays results.
    """

    compression = Query()
    user_request = input("What do you want to search in the filenames contained in the history ? ")
    if results := database.DB.search(compression.filename.search(user_request)):
        print("Here's the list of all matching files in the history:")
        for entry in results:
            print(f"{entry['date']}: \n{typer.style(entry['filename'], fg=typer.colors.YELLOW)}")
    else:
        print(f"No match with '{user_request}' found in the filenames.")


@check_empty_db
def display():
    """Displays the entire history."""

    print("Here's the list of all successful compressions "
          "realized since last clearing:")
    for entry in iter(database.DB):
        print(f"{entry['date']}: "
              f"{typer.style(entry['filename'], fg=FAKE.color_rgb())}")


@check_empty_db
def clear():
    """Clears the history"""

    message = "Are you sure you want to clear your compression history ? [y/N] "
    user_choice = input(message)
    if user_choice.upper() == 'Y':
        database.DB.truncate()
        print("Your history is cleared.")


if __name__ == "__main__":
    display()
