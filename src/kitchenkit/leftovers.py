from dataclasses import dataclass

from .pantry import Food


@dataclass
class Meatloaf(Food):
    microwave_duration: int = 3


@dataclass
class Bulgur(Food):
    microwave_duration: int = 2


@dataclass
class RoastedChicken(Food):
    microwave_duration: int = 4


@dataclass
class Pizza(Food):
    microwave_duration: int = 3


@dataclass
class Turkey(Food):
    microwave_duration: int = 5
