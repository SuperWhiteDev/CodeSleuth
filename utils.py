import sys
import os

def convert_to_rgb(string : str) -> tuple[int, int, int]:
    """
    Converts a string in the format “rgb(red, green, blue)” to a tuple of three integers (red, green, blue).
    """

    try:
        red, green, blue = string.replace("rgb(", "").replace(")", "").split(", ")
    
        red = int(red)
        green = int(green)
        blue = int(blue)
        return (red, green, blue)
    except Exception:
        return (255, 255, 255)
    
def resource_path(relative_path : str):
    """
    Gets the absolute path to the resource, works in both development and compiled mode.

    :param relative_path: path to resource
    :return: path
    """

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)