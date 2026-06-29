import asyncio
from collections.abc import Callable, Coroutine
import time

from .context import started_at
from .exceptions import MessyKitchenError
from .logging import logger
from .pantry import Food

__all__ = [
    "async_cook",
    "async_microwave",
    "cook",
    "microwave",
    "peel_and_slice",
]


def _kitchen_function_factory[F: Food](action_name: str) -> Callable[[F], F]:
    def kitchen_function(food: F) -> F:
        if started_at.get() is None:
            raise MessyKitchenError(f"Can't {action_name} without your apron on!")

        func_name = action_name.replace(" ", "_")
        attr_name = func_name + "_duration"
        if getattr(food, attr_name) is None:
            raise MessyKitchenError(f"{food.name.capitalize()} can't go into {func_name}.")

        logger.info("Going to %s the %s.", action_name, food.name)
        time.sleep(getattr(food, attr_name, 0))
        logger.info("The %s is ready!", food.name)
        food.handled += 1
        return food
    return kitchen_function


cook = _kitchen_function_factory("cook")
microwave = _kitchen_function_factory("microwave")
peel_and_slice = _kitchen_function_factory("peel and slice")


_MICROWAVE_LOCK = asyncio.Lock()
_COOK_SEMAPHORE = asyncio.Semaphore(2)


def _async_kitchen_function_factory[F: Food](action_name: str) -> Callable[[F], Coroutine[None, None, F]]:
    async def kitchen_function(food: F) -> F:
        if started_at.get() is None:
            raise MessyKitchenError(f"Can't {action_name} without your apron on!")

        func_name = action_name.replace(" ", "_")
        attr_name = func_name + "_duration"
        if getattr(food, attr_name) is None:
            raise MessyKitchenError(f"{food.name.capitalize()} can't go into {func_name}.")

        # Special case for the veggies that need to be peeled/sliced before cooking.
        if action_name == "cook" and getattr(food, "peel_and_slice_duration", 0) and not food.handled:
            raise MessyKitchenError(f"Did you forget to peel/slice the {food.name}?")

        logger.info("Going to %s the %s.", action_name, food.name)
        logger.info("What can I do to save time..?")
        await asyncio.sleep(getattr(food, attr_name, 0))
        logger.info("The %s is ready!", food.name)
        food.handled += 1
        return food

    return kitchen_function


_async_microwave = _async_kitchen_function_factory("microwave")
async def async_microwave[F: Food](food: F) -> F:
    if _MICROWAVE_LOCK.locked():
        raise MessyKitchenError("There's already something in the microwave!")

    async with _MICROWAVE_LOCK:
        return await _async_microwave(food)


_async_cook = _async_kitchen_function_factory("cook")
async def async_cook[F: Food](food: F) -> F:
    if _COOK_SEMAPHORE.locked():
        raise MessyKitchenError("The two pots are already in use!")

    async with _COOK_SEMAPHORE:
        return await _async_cook(food)
