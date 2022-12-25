import logging

from mppsolar.helpers import get_kwargs, key_wanted

from .helpers import get_common_params
from .mqtt import MQTT

log = logging.getLogger("tag_mqtt")


class TagMQTT(MQTT):
    def __str__(self):
        return "outputs the to the supplied mqtt broker using the supplied tag as the topic: eg {tag}/max_charger_range 120.0"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)

        _topic = get_kwargs(kwargs, "topic", default="mpp-solar")

        # Build array of Influx Line Protocol II messages
        # Message format is: mpp-solar,command=QPGS0 max_charger_range=120.0
        #                    mpp-solar,command=inverter2 parallel_instance_number="valid"
        #                    measurement,tag_set field_set
        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        if tag is None:
            tag = cmd
        # Loop through responses
        for key in data:
            value = data[key][0]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter_, excl_filter):
                msg = {
                    "topic": f"{tag}/{key}",
                    "payload": value,
                }
                msgs.append(msg)
        return msgs
