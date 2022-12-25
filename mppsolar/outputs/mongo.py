import datetime
import logging

from mppsolar.helpers import get_kwargs

from .baseoutput import BaseOutput
from .helpers import get_common_params, to_json

log = logging.getLogger("mongo")

try:
    import pymongo as pymongo
except ImportError:
    log.warning("MongoDB output is not awailable")


class Mongo(BaseOutput):
    def __str__(self):
        return "outputs all the results to MongoDB"

    def output(self, *args, **kwargs):
        data, tag, keep_case, filter_, excl_filter = get_common_params(kwargs)

        mongo_url = get_kwargs(kwargs, "mongo_url")
        mongo_database = get_kwargs(kwargs, "mongo_db", "mppsolar")
        log.debug(f"Connecting to {mongo_url} / {mongo_database}")
        client = pymongo.MongoClient(mongo_url)
        db = client[mongo_database]

        msgs = []
        # Remove command and _command_description
        # cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        # if tag is None:
        #     tag = cmd
        output = to_json(data, keep_case, excl_filter, filter_)

        log.debug(output)
        msgs.append(output)
        inserted = 0
        try:
            for msg in msgs:
                col = msg.pop("_command")
                msg["updated"] = datetime.datetime.now()
                result = db[col].insert_one(msg)
                if result is not None:
                    log.debug(result.inserted_id)
                    inserted += 1
            log.debug(f"inserted {inserted} docs")
        except pymongo.errors.ServerSelectionTimeoutError as dbe:
            log.error(f"Mongo error {dbe}")
        return msgs
