from dataclasses import dataclass
from typing import Optional

@dataclass
class Car:
    id: Optional[int] = None
    brand: str = ""
    model: str = ""
    year: int = 0
    color: str = ""
    plate: str = ""
