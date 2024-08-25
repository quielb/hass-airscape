# AirScape Whole House Fan  [![hacs][hacsbadge]][hacs]

[![Github Release][release-shield]][releases]
![issues]

A Home Assistant custom component to integrate [Airscape Whole House Fans][airscape-url] with Gen2 controls.

## Installation via HACS (recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=quielb&repository=hass-airscape)

1. Follow the link [here](https://hacs.xyz/docs/faq/custom_repositories/)
2. Use the custom repo link https://github.com/quielb/hass-airscape
3. Select the category type `integration`
4. Then once it's there (still in HACS) click the INSTALL button
5. Restart Home Assistant
6. Once restarted, in the HA UI go to `Configuration` (the ⚙️ in the lower left) -> `Devices and Services` click `+ Add Integration` and search for `airscape`

## Using the Airscape component

The basic component operation of the component implements all the features of the fan component. This integration extends the basic fan adding additional functionality specific to an Airscape whole house fan.

**Services**

The Airscape component has several custom services that are controlled by the minimum speed configuration option:

Service | Description
-- | --
`airscape.turn_on_to_minimum` | Starts the fan and sets the speed to the minimum defined configuration option
`airscape.speed_up` | Increase the fan speed by one step
`airscape.slow_down` | Slow down the fan speed by one step. Will not go below the defined minimum fan speed configuration option

**Controls**

In addition to the standard fan controls there is one addition button. When used, the button will add one hour to the timer.

**Sensors**

The Airscape component adds several sensors to represent the data from the fan:

Sensor | Description
-- | --
Attic Temperature | Readings from Attic temp sensor
CFM | Current CFM of fan
Power | Power usage in Watts
Timer Remaining | Number of minutes remaining on shutoff timer
Inside | Reading from control panel wall plate (disabled by default)
Outside | Readings from deprecated outdoor data collection kit (disabled by default)
Door | Binary sensor to indicate if fan doors are in motion (disabled by default)

[airscape-url]: https://airscapefans.com/
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[releases]: https://github.com/quielb/hass-airscape/releases
[release-shield]: https://img.shields.io/github/v/release/quielb/hass-airscape
[issues]: https://img.shields.io/github/issues/quielb/hass-airscape
