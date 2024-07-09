import yaml
import os

script_cache = {}  # Cache for the content of JavaScript files


def initialize_scripts(yaml_file: str = "SCRIPT_PATHS.yaml") -> None:
    """
    Load and cache JavaScript files into memory from a YAML file.
    MUST BE CALLED BEFORE EXECUTING ANY JS SCRIPTS.
    :param yaml_file: Path to the YAML file containing script names and paths.
    :return: None
    """
    script_names = _load_script_names_from_yaml(yaml_file)
    _load_js_scripts(script_names)


def get_script_cache() -> dict[str, str]:
    """
    Get the cache of JavaScript files.
    :return: Dictionary of script names and file paths.
    """
    global script_cache
    return script_cache


def _load_script_names_from_yaml(yaml_file: str) -> dict[str, str]:
    """
    Load script names and paths from a YAML file.
    :param yaml_file: Path to the YAML file.
    :return: Dictionary of script names and file paths.
    """
    try:
        with open(yaml_file, 'r') as file:
            return yaml.safe_load(file)
    except:
        return {}


def _load_js_scripts(script_names: dict[str, str]) -> None:
    """
    Load and cache JavaScript files into memory.
    :param script_names: Dictionary of script names and file paths.
    :return: None
    """
    global script_cache
    for name, path in script_names.items():
        if not os.path.isfile(path):
            print(f"The script file '{path}' does not exist.")
            continue
        try:
            with open(path, 'r') as file:
                script_cache[name] = file.read()
        except Exception as e:
            print(f"The script file '{path}' could not be read.")
            print(e)


initialize_scripts()
