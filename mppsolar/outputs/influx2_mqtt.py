import logging

from mppsolar.helpers import get_kwargs, key_wanted

from .helpers import get_common_params
from .mqtt import MQTT

log = logging.getLogger(__name__)


class Influx2MQTT(MQTT):
    def __str__(self):
        return "outputs the to the supplied mqtt broker: eg mpp-solar,command={tag} max_charger_range=120.0"

    def build_msgs(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)
        topic = get_kwargs(kwargs, "mqtt_topic", default="mpp-solar")

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
                if isinstance(value, int) or isinstance(value, float):
                    msg = {
                        "topic": topic,
                        "payload": f"{topic},command={tag} {key}={value}",
                    }
                else:
                    msg = {
                        "topic": topic,
                        "payload": f'{topic},command={tag} {key}="{value}"',
                    }
                msgs.append(msg)
        return msgs
