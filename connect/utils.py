"""The main app utils."""

import binascii


def transform_literal_id(literal_id: str):
    """Transform given literal id into hexadecimal integer."""
    return int(
        binascii.hexlify(bytes(literal_id, encoding="utf-8")).decode("utf-8"), 18
    )
