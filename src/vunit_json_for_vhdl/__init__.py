"""
Helping functions for JSON handling in VUnit projects.

For more information, see the README.md file.
"""

from pathlib import Path
from typing import Union
import json
from base64 import b16encode as b16enc


def encode_json(obj: object):
    """
    Convert object to stringified JSON.

    :param obj: Object to stringify

    :example:

    .. code-block:: python

       stringified_generic = encode_json(generics)
    """
    return json.dumps(obj, separators=(",", ":"))


def read_json(filename: str):
    """
    Read a JSON file and return an object.

    :param filename: The name of the file to read

    :example:

    .. code-block:: python

       generics = read_json(join(root, "src/test/data/data.json"))
    """
    with Path(filename).open("r", encoding="utf-8") as fptr:
        return json.loads(fptr.read())


def b16encode(data: Union[str, bytes]):
    """Encode a str|bytes using Base16 and return a str|bytes."""
    if isinstance(data, str):
        return b16enc(bytes(data, "utf-8")).decode("utf-8")
    return b16encode(data)


def to_str(obj: object) -> str:
    """
    Convert object to stringified JSON and then Base16 encode it.

    :param obj: Object to convert

    :example:

    .. code-block:: python

       hex_generic = to_hex(generics)
    """
    json_str = encode_json(obj)
    return b16encode(json_str)
