import asyncio
from collections.abc import Callable, Coroutine

from .context import started_at
from .exceptions import MessyKitchenError
from .logging import logger
from .pantry import Food
from .prep import peel_and_slice as _sync_peel_and_slice


__all__ = [
    "cook",
    "microwave",
    "peel_and_slice",
]

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

        logger.info("Going to %s the %s.", action_name, food.name)
        logger.info("What can I do to save time..?")
        await asyncio.sleep(getattr(food, attr_name, 0))
        logger.info("The %s is ready!", food.name)
        food.handled += 1
        return food

    return kitchen_function


_cook = _async_kitchen_function_factory("cook")
_microwave = _async_kitchen_function_factory("microwave")


async def microwave[F: Food](food: F) -> F:
    if _MICROWAVE_LOCK.locked():
        raise MessyKitchenError("There's already something in the microwave!")

    async with _MICROWAVE_LOCK:
        return await _microwave(food)


async def cook[F: Food](food: F) -> F:
    if _COOK_SEMAPHORE.locked():
        raise MessyKitchenError("The two pots are already in use!")

    async with _COOK_SEMAPHORE:
        return await _cook(food)


async def peel_and_slice[F: Food](food: F) -> F:
    return _sync_peel_and_slice(food)
