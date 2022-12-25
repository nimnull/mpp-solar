import logging

from mppsolar.helpers import get_kwargs, key_wanted

from .helpers import get_common_params
from .mqtt import MQTT

log = logging.getLogger(__name__)


class InfluxMQTT(MQTT):
    def __str__(self):
        return """outputs the to the supplied mqtt broker: eg {tag}, {tag},setting=total_ac_output_apparent_power value=1577.0,unit="VA" """

    def build_msgs(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)
        topic = get_kwargs(kwargs, "mqtt_topic", default="mpp-solar")

        # Build array of Influx Line Protocol messages
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
            unit = data[key][1]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            # Message format is: tag, tag,setting=total_ac_output_apparent_power value=1577.0,unit="VA"
            if key_wanted(key, filter_, excl_filter):
                if not unit:
                    msg = {
                        "topic": topic,
                        "payload": f"{tag},setting={key} value={value}",
                    }
                else:
                    msg = {
                        "topic": topic,
                        "payload": f"{tag},setting={key} value={value},unit={unit}",
                    }
                msgs.append(msg)
        return msgs
