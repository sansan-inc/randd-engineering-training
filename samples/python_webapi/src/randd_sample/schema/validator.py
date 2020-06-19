import functools
import json
from pathlib import Path

import jsonschema


def load_schema(filename):
    with open(filename, "rt") as f:
        return json.load(f)


validate_sample_request = functools.partial(
    jsonschema.validate,
    schema=load_schema(
        Path(__file__).parent.joinpath(
            "json",
            "sample_request-1.0.0.json"
        )
    )
)
