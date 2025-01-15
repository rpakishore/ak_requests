from dataclasses import dataclass


@dataclass
class Cookie:
    """Cookie class for storing cookie information."""

    name: str
    value: str
