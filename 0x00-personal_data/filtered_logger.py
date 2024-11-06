#!/usr/bin/env python3
"""
Module for filtering PII fields in log messages.
"""

import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str,
        separator: str) -> str:
    """
    Replace values of certain fields in a log message with a redaction string.

    Args:
        fields: List of fields to redact.
        redaction: String to replace the field values with.
        message: The log message.
        separator: The separator used between fields.

    Returns:
        The redacted log message.
    """
    pattern = '|'.join([f"{field}=[^;]*" for field in fields])
    return re.sub(
            pattern,
            lambda x: x.group().split('=')[0] + '=' + redaction,
            message)
