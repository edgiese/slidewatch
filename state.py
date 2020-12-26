

state_definition = {}
current_state_number = 0
current_slide = -1
channels = [
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
    {"name": "undefined", "muted": False, "level": 100, "overridden": False},
]
defined_scenes = []
current_state_name = ""


def init(data):
    global state_definition
    global current_state_number
    current_state_number = 0
    state_definition = data

def bump_state():
    global current_state_number
    current_state_number = current_state_number + 1

def get_current():
    if -1 == current_slide:
        return state_definition["defines"]["states"][current_slide]
    return {"name": "default", "scene": "4 Camera", "presets": [], "mics": []}


def set_slide(current):
    global current_slide
    current_slide = current-1
