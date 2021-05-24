# AirScape Whole House Fan [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom component to control Airscape Whole House Fans with Gen2 controls.

{% if installed %}

### Breaking Changes

{% if version_installed.replace("v", "").replace(".","") | int < 190  %}

- Removed speed_up and slow_down custom services now that new FanEntity has them built in.
  {% endif %}

### Changes

{% if version_installed.replace("v", "").replace(".","") | int < 190  %}

- Added the ability to dynamically determine max speed based on model. Should allow for speed to be correctly represented in the Front End.
- Updated Entity to utilized the new percentage speed model in HA.
  {% endif %}
  {% endif %}

{% if not installed %}

### Installation

1. Click install.
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Blueprint".

{% endif %}

### Usage

Add to configuration.yaml

```yaml
fan:
  - platform: airscape
    name: Whole House
    host: "192.168.10.249"
    minimum: 4
```

The minimum attribute is optional. It specifies the minimum starting speed and prevents the speed from going below that value.

This component adds one custom service:

```
airscape.add_time
```

This allows for adding an hour of time to the timer on the fan.
