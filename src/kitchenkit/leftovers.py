from dataclasses import dataclass

from .pantry import Food


@dataclass
class Meatloaf(Food):
    microwave_duration: int = 3


@dataclass
class Couscous(Food):
    microwave_duration: int = 3
