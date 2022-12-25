import logging

from mppsolar.helpers import key_wanted

from .baseoutput import BaseOutput
from .helpers import get_common_params

log = logging.getLogger("screen")


class Screen(BaseOutput):
    def __str__(self):
        return "[the default output module] outputs the results to standard out in a slightly formatted way"

    def output(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)

        if data is None:
            return

        _desc = "No description found"
        if "_command_description" in data:
            _desc = data["_command_description"]
            del data["_command_description"]
        if "_command" in data:
            print(f"Command: {data['_command']} - {_desc}")
            print("-" * 60)
            del data["_command"]
        if "raw_response" in data:
            del data["raw_response"]

        print(f"{'Parameter':<30}\t{'Value':<15} Unit")
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter_, excl_filter):
                try:
                    print(f"{key:<30}\t{value:<15}\t{unit:<4}")
                except TypeError:
                    print(key, value, unit)
