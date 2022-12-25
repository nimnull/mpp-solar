import json as js
import logging

from mppsolar.helpers import get_kwargs

from .helpers import get_common_params, to_json
from .mqtt import MQTT

log = logging.getLogger(__name__)


class JsonMQTT(MQTT):
    def __str__(self):
        return "outputs all the results to the supplied mqtt broker in a single message formatted as json: eg "

    def build_msgs(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)

        mqtt_broker = get_kwargs(kwargs, "mqtt_broker")
        if mqtt_broker is not None:
            topic = mqtt_broker.results_topic
        else:
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
        output = to_json(data, keep_case, excl_filter, filter_)
        payload = js.dumps(output)
        msg = {
            "topic": topic,
            "payload": payload,
        }
        msgs.append(msg)
        return msgs
