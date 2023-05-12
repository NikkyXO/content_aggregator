from __future__ import annotations
from typing import Any


class ThirdPartyAPIConnectionError(Exception):
    def __init__(self, response_code: int, response_data: dict[str, Any]):
        """Set response code and response data."""
        self.response_code = response_code
        self.response_data = response_data
        super().__init__("ThirdPartyAPIConnectionError")