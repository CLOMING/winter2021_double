from _typeshed import OpenBinaryMode
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DoubleError(Exception):
    message: str
    data: Optional[Any] = None

    def __str__(self) -> str:
        error_message: str = f'[DoubleError] {self.message}'

        if not self.data:
            error_message += f'\n{self.data}'

        return error_message
