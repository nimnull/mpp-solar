import logging

from mppsolar.helpers import key_wanted

from .helpers import get_common_params
from .mqtt import MQTT

log = logging.getLogger(__name__)


class DomoticzMQTT(MQTT):
    def __str__(self):
        return """outputs the to the supplied mqtt broker in hass format: eg "homeassistant/sensor/mpp_{tag}_{key}/state" """

    def build_msgs(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)

        # Build array of mqtt messages with hass update format
        # assumes hass_config has been run
        # or hass updated manually
        msgs = []
        # Remove command and _command_description
        data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)

        # Loop through responses
        for _key in data:
            value = data[_key][0]
            unit = data[_key][1]
            # remove spaces
            key = _key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                #
                # CONFIG / AUTODISCOVER
                #
                # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
                # topic "homeassistant/binary_sensor/garden/config"
                # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C"}'
                # topic = f"homeassistant/sensor/mpp_{tag}_{key}/config"
                # topic = topic.replace(" ", "_")
                state_topic = f"domoticz/sensor/mpp_{tag}_{key}/state"
                state_topic = state_topic.replace(" ", "_")

                # name = f"{tag} {_key}"
                # if unit == "W":
                #     payload = f'{{"name": "{name}", "stat_t": "{state_topic}", "unit_of_meas": "{unit}", "uniq_id": "mpp_{tag}_{key}", "stat_cla": "measurement", "device_class": "power"  }}'
                # else:
                #     payload = f'{{"name": "{name}", "stat_t": "{state_topic}", "unit_of_meas": "{unit}", "uniq_id": "mpp_{tag}_{key}"  }}'
                # # msg = {"topic": topic, "payload": payload, "retain": True}
                # msg = {"topic": topic, "payload": payload}
                # msgs.append(msg)
                #
                # VALUE SETTING
                #
                if unit in ("A", "V", "%", "W"):
                    payload = f"{value} {unit}"
                else:
                    payload = value
                msg = {"topic": state_topic, "payload": payload}
                msgs.append(msg)
        return msgs
