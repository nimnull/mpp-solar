import json as js
import logging
import socket

from mppsolar.helpers import get_kwargs

from .baseoutput import BaseOutput
from .helpers import get_common_params, to_json

log = logging.getLogger("json_udp")


class JsonUDP(BaseOutput):
    def __str__(self):
        return "outputs all the results to tcp UDP datagram packet in JSON format"

    def output(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)
        udp_port = get_kwargs(kwargs, "udp_port", "5555")

        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)

        output = to_json(data, keep_case, excl_filter, filter_)

        payload = js.dumps(output)
        log.debug(payload)
        msgs.append(payload)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP datagram
        for msg in msgs:
            count = sock.sendto(bytes(msg, "utf-8"), ("localhost", int(udp_port)))
            log.debug(f"Udp sent response {count}")
        return msgs
