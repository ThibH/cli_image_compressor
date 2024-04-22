import ui
import functions
import history
import main

DEFAULT_QUALITY = 75
OPTIONS = {
    1: {"display": "Know more about this software", "function": ui.display_info_message},
    2: {"display": "Compress image(s)", "function": main.compress},
    3: {"display": "Search in the history", "function": history.search},
    4: {"display": "Display the history", "function": history.display},
    5: {"display": "Clear the history", "function": history.clear},
    6: {"display": "Quit", "function": ui.display_goodbye_message},
}
