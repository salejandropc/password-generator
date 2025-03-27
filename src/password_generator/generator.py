import random
import string
from enum import Enum


class Methods(Enum):
    RANDOM = 1


class PasswordGenerator:
    def __init__(
        self, method: str, length: int = 12, use_symbols: bool = False
    ) -> None:
        self.method = method
        self.length = length
        self._use_symbols = use_symbols
        self._sanity_checks()

    def _sanity_checks(self) -> None:
        if self.method not in self.methods:
            raise ValueError(
                f"Method {self.method} is not supported! Supported methods are {self.methods}"
            )

    @property
    def characters(self):
        if self._use_symbols:
            return string.ascii_letters + string.digits + string.punctuation
        return string.ascii_letters + string.digits

    @property
    def methods(self) -> list[str]:
        return [item.name for item in Methods]

    def random_generation(self) -> str:
        return "".join(random.choice(self.characters) for _ in range(self.length))

    def generate(self) -> str:
        if self.method == Methods.RANDOM.name.lower():
            return self.random_generation()
        else:
            raise RuntimeError("Unsupported method!")
