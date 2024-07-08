from selenium.webdriver.remote.webdriver import WebDriver
import yaml
import os

from bannerdriver.functions_general import switch_iframe, get_driver
from bannerdriver.drivers.driver_base import BannerDriver

script_cache = {}  # Cache for the content of JavaScript files


def initialize_scripts(yaml_file: str) -> None:
    """
    Load and cache JavaScript files into memory from a YAML file.
    :param yaml_file: Path to the YAML file containing script names and paths.
    :return: None
    """
    script_names = _load_script_names_from_yaml(yaml_file)
    _load_js_scripts(script_names)


def _load_script_names_from_yaml(yaml_file: str) -> dict[str, str]:
    """
    Load script names and paths from a YAML file.
    :param yaml_file: Path to the YAML file.
    :return: Dictionary of script names and file paths.
    """
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)


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
            continue


def execute_js(driver: WebDriver | BannerDriver, script_name: str, *args) -> any:
    """
    Executes a cached JavaScript file on the current page using Selenium WebDriver.
    :param driver: WebDriver object.
    :param script_name: Name of the cached JavaScript script to execute.
    :param args: Arguments to pass to the JavaScript function.
    :raises ValueError: If the script name is invalid or scripts are not loaded.
    :return: Result of the executed script or None.
    """
    if not script_cache:
        raise ValueError("No JavaScript scripts have been loaded.")
    driver = get_driver(driver)
    switch_iframe(driver)
    js_script = script_cache.get(script_name)

    if not js_script:
        raise ValueError(f"Invalid script name '{script_name}'")

    try:
        js_code = f"return {js_script};"
        result = driver.execute_script(js_code, *args)
        return result
    except Exception as e:
        raise Exception(f"Error executing the script '{script_name}': {e}")
