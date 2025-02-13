import json
import os

CODESLEUTH_FOLDER = r"C:\ProgramData\CodeSleuth"
CONFIG_FILE = os.path.join(CODESLEUTH_FOLDER, r"config.json")

def check_folder():
    if not os.path.exists(CODESLEUTH_FOLDER):
        os.makedirs(CODESLEUTH_FOLDER)

def get_config():
    try:
        with open(CONFIG_FILE, "r", encoding="UTF-8") as f:
            config = json.load(f)
    
        return config
    except Exception:
        return {}
    
def save_config(config : dict):
    with open(CONFIG_FILE, "w", encoding="UTF-8") as f:
        json.dump(config, f, indent=4)

def save_search_paths(paths : list):
    check_folder()

    config = get_config()
    config["search_paths"] = paths
    
    save_config(config)
    
def save_search_exeption_paths(paths : list):
    check_folder()

    config = get_config()
    config["search_exeption_paths"] = paths
    
    save_config(config)
        
def save_search_limits(limits : dict):
    check_folder()

    config = get_config()
    config["search_limits"] = limits
    
    save_config(config)
        
def save_theme(theme_file : str):
    check_folder()

    config = get_config()
    config["theme"] = theme_file
    
    save_config(config)

def get_search_paths() -> list:
    try:
        return get_config()["search_paths"]
    except Exception:
        return []
    
def get_search_exeption_paths() -> list:
    try:
        return get_config()["search_exeption_paths"]
    except Exception:
        return []
    
def get_search_limits() -> dict:
    try:
        return get_config()["search_limits"]
    except Exception:
        return {}

def get_theme_file() -> str:
    try:
        return get_config()["theme"]
    except Exception:
        return None
    
def get_theme_files() -> str:
    theme_files = []
    
    for root, dirs, files in os.walk(os.path.join(CODESLEUTH_FOLDER, "Themes")):
        for file in files:
            theme_files.append(file)
    return theme_files
def get_theme() -> str:
    file = get_theme_file()
    
    if file:
        try:
            with open(os.path.join(CODESLEUTH_FOLDER, "Themes", file), "r", encoding="UTF-8") as f:
                theme = json.load(f)
        except Exception:
            return "Default"
        
        if "name" in theme:
            return theme["name"]
        else:
            return "Unnamed"
    
    return "Default"

def get_widget_style(widget : str, style : str) -> str:
    file = get_theme_file()
    
    if file:
        try:
            with open(os.path.join(CODESLEUTH_FOLDER, "Themes", file), "r", encoding="UTF-8") as f:
                theme = json.load(f)

                if widget in theme:
                    if style in theme[widget]:
                        return theme[widget][style]
                    
                return None
        except Exception:
            return None

    else:
        return None
