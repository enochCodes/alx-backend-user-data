#!/usr/bin/env python3
"""Filtered logger module
return logger object with filter."""
import logging
import re
from typing import List


def filter_datum(
    fileds: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """Filter a datum."""
    pattern = r'(' + '|'.join(
        map(re.escape, fileds)) + ')=(.*?)(?=' + separator + ')'
    return re.sub(pattern, r'\1=' + redaction, message)
