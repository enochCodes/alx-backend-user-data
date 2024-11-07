#!/usr/bin/env python3
"""Filtered logger module
return logger object with filter."""
import logging
import re
from typing import List
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)

    @staticmethod
    def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
    ) -> str:
        """Obfuscate the values of specified fields in a log message."""
        for f in fields:
            message = re.sub(
                f'{f}=.*?{separator}', f'{f}={redaction}{separator}', message)
            return message


def get_logger() -> logging.Logger:
    """ Returns a configured logger with
   specific settings. """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger

def get_db() -> MySQLConnection:
    """Establishes and returns a connection to the database."""
    # Retrieve environment variables with default values
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the database and return the connection object
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
