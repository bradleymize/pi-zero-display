import importlib
import inspect
import logging

# TODO: import separate logging module so instantiated no matter where its used
log = logging.getLogger(__name__)

DISPLAY = None
SCREENS = {}
CURRENT_PAGE = None


def set_display(display):
    global DISPLAY
    DISPLAY = display


def get_display():
    return DISPLAY


def get_current_page():
    return CURRENT_PAGE


def set_current_page(page):
    global CURRENT_PAGE
    CURRENT_PAGE = page


# TODO: change print to info.debug
def instantiate_screens():
    all_classes = []

    # Load the root module for all the commands
    package = importlib.import_module("screens")

    # Get all the members of the module (specifically __all__, populated by package's __init__.py)
    contents = inspect.getmembers(package, lambda x: not inspect.isroutine(x))
    all_modules = [list(c[1]) for c in contents if c[0] == "__all__"][0]

    # print("Loading screen module")

    for module in all_modules:
        module_name = f"screens.{module}"
        # Dynamically import the command module
        package = importlib.import_module(module_name)
        contents = inspect.getmembers(package, lambda x: inspect.isclass(x))
        # Get all the classes belonging directly to the module
        classes = [c[1] for c in contents if inspect.isclass(c[1]) and c[1].__module__ == module_name]
        # print(f"module_name: {module_name}")
        # print(f"classes: {classes}")
        # Add the classes to the list of all the classes in the module
        all_classes = all_classes + classes

    # print(f"all_classes: {all_classes}")

    for c in all_classes:
        # print(f"Instantiating screen: {c.__name__}")
        SCREENS[c.__name__] = c()


instantiate_screens()
