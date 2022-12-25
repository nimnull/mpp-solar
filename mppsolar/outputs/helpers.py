import re

from mppsolar.helpers import get_kwargs, key_wanted


def get_common_params(kwargs):
    data = get_kwargs(kwargs, "data")
    tag = get_kwargs(kwargs, "tag")
    keep_case = get_kwargs(kwargs, "keep_case")
    filter_ = get_kwargs(kwargs, "filter")
    if filter_ is not None:
        filter_ = re.compile(filter_)
    excl_filter = get_kwargs(kwargs, "excl_filter")
    if excl_filter is not None:
        excl_filter = re.compile(excl_filter)
    return data, tag, keep_case, filter_, excl_filter


def to_json(data, keep_case, excl_filter, filter):
    output = {}
    # Loop through responses
    for key in data:
        value = data[key]
        if isinstance(value, list):
            value = data[key][0]
        # unit = data[key][1]
        # remove spaces
        key = key.replace(" ", "_")
        if not keep_case:
            # make lowercase
            key = key.lower()
        if key_wanted(key, filter, excl_filter):
            output[key] = value
    return output
