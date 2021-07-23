DEFAULT_TIMEOUT = 5
DEFAULT_MINIMUM = 1
DEFAULT_MAXIMUM = -1 # -1 to use the maximum returned by the airscape.Fan.max_speed
fan_to_hass_attr = {
    "doorinprocess": "Door Moving",
    "cfm": "CFM",
    "power": "Power",
    "inside": "Inside Temperature",
    "attic": "Attic Temperature",
    "oa": "Outside Temperature",
    "interlock1": "InterLock1",
    "interlock2": "InterLock2",
    "timeremaining": "Shutoff Timer",
}
