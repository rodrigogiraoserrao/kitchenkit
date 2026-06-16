from dataclasses import dataclass

from .context import ingredients

@dataclass
class Food:
    handled: int = 0
    cook_duration: int | None = None
    microwave_duration: int | None = None
    peel_and_slice_duration: int | None = None
    name: str = "food"

    def __post_init__(self) -> None:
        self.name = type(self).__name__.lower()
        ingredients.set(ingredients.get() + 1)


@dataclass
class Avocado(Food):
    peel_and_slice_duration: int = 2


@dataclass
class Tomato(Food):
    peel_and_slice_duration: int = 2


@dataclass
class Onion(Food):
    peel_and_slice_duration: int = 2


@dataclass
class Broccoli(Food):
    peel_and_slice_duration: int = 2
    cook_duration: int = 5


@dataclass
class Carrots(Food):
    peel_and_slice_duration: int = 2
    cook_duration: int = 5


@dataclass
class Leek(Food):
    peel_and_slice_duration: int = 2
    cook_duration: int = 5


@dataclass
class GreenBeans(Food):
    peel_and_slice_duration: int = 2
    cook_duration: int = 5


@dataclass
class Asparagus(Food):
    peel_and_slice_duration: int = 2
    cook_duration: int = 5


@dataclass
class Pasta(Food):
    cook_duration: int = 10


@dataclass
class Rice(Food):
    cook_duration: int = 10


@dataclass
class Couscous(Food):
    cook_duration: int = 10
