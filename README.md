# AirScape Whole House Fan [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom component to control Airscape Whole House Fans with Gen2 controls.

To Add a fan update your configuration.yaml:

```yaml
fan:
  - platform: airscape
    name: Whole House
    host: "192.168.10.249"
```

There is one other attribute supported. Setting a minimum speed value will start up the WHF with that speed and prevent any automation from reducing the speed below the minimum.

```yaml
fan:
  - platform: airscape
    name: Whole House
    host: "192.168.10.249"
    minimum: 4
```

This component adds one custom service:

```
airscape.add_time
```

This allows for adding an hour of time to the timer on the fan.
