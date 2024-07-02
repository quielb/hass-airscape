# AirScape Whole House Fan [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom component to control Airscape Whole House Fans with Gen2 controls.

{% if installed %}

### Breaking Changes

{% if version_installed.replace("v", "").replace(".","") | int < 194  %}

- Fixed attribute names to be more consistent with HA standards. They are now all lowercase and no longer include spaces.
  {% endif %}

{% if version_installed.replace("v", "").replace(".","") | int < 190  %}

- Removed speed_up and slow_down custom services now that new FanEntity has them built in.
  {% endif %}

### Changes
{% if version_installed.replace("v", "").replace(".","") | int < 1955  %}

- Adding unique ids to all fan entities which will allow them to be configured via the UI.
  {% endif %}


{% if version_installed.replace("v", "").replace(".","") | int < 1951  %}

- Bump pypi airscape to v0.1.9.4.1 for speed of 4.4eWHF fan
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 195  %}

- Bump pypi airscape to v0.1.9.4 to support fans that don't have a status.cgi.
  {% endif %}

{% if version_installed.replace("v", "").replace(".","") | int < 194  %}

- Small update to fix additional attributes not showing up.
  {% endif %}

{% if version_installed.replace("v", "").replace(".","") | int < 193  %}

- Reverted the removal of custom services slow_down and speed_up. The built in service fan.decrease_speed allows the fan to be turned off
  if decreased_speed is at the minimum speed.
  {% endif %}

{% if version_installed.replace("v", "").replace(".","") | int < 190  %}

- Added the ability to dynamically determine max speed based on model. Should allow for speed to be correctly represented in the Front End.
- Updated Entity to utilized the new percentage speed model in HA.
  {% endif %}
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

This component adds three custom service:

```
airscape.speed_up
airscape.slow_down
airscape.add_time
```
