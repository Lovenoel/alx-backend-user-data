#!/usr/bin/env python3
"""
Module for filtering PII fields in log messages.
"""

import re
import logging
from typing import List, Tuple
import os
import mysql.connector
from mysql.connector import connection


def get_db() -> connection.MySQLConnection:
    """ Connect to the MySQL database using environment variables. """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for log messages. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Apply filter_datum to the log record message. """
        return filter_datum(
                self.fields, self.REDACTION,
                super().format(record), self.SEPARATOR)


PII_FIELDS: Tuple[str, ...] = (
        "name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """ Set up a logger with redacted fields. """
    logger: logging.Logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger
