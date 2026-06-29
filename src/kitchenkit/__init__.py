import asyncio
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from functools import wraps
import time

from .context import ingredients, started_at
from .exceptions import MessyKitchenError
from .logging import logger
from .leftovers import Meatloaf, Bulgur, RoastedChicken, Pizza, Turkey
from .pantry import (
    Food,
    Avocado,
    Broccoli,
    Tomato,
    Onion,
    Carrots,
    Leek,
    GreenBeans,
    Asparagus,
    Pasta,
    Rice,
    Couscous,
)
from .prep import async_cook, async_microwave, cook, microwave, peel_and_slice

__all__ = [
    "put_on_apron",
    "serve_food",
    "Food",
    "Avocado",
    "Broccoli",
    "Tomato",
    "Onion",
    "Carrots",
    "Leek",
    "GreenBeans",
    "Asparagus",
    "Pasta",
    "Rice",
    "Couscous",
    "Meatloaf",
    "Bulgur",
    "RoastedChicken",
    "Pizza",
    "Turkey",
    "async_cook",
    "async_microwave",
    "cook",
    "microwave",
    "peel_and_slice",
]


def put_on_apron() -> None:
    logger.info("Let's get cooking! 🧑‍🍳")
    started_at.set(time.perf_counter())


def serve_food(*food: Food) -> None:
    for item in food:
        if not item.handled:
            raise MessyKitchenError(f"Did you forget to prepare the {item.name}?")

    if len(food) < ingredients.get():
        raise MessyKitchenError("Did you serve all your food?")

    start = started_at.get()
    if start is None:
        raise MessyKitchenError("Can't serve food if you prepared nothing!")
    elapsed = time.perf_counter() - start
    logger.info("Finished cooking in %ds. ✨", round(elapsed))
    logger.info("Now serving: %s", ", ".join(f.name for f in food))
