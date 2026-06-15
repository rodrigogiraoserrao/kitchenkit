from collections.abc import Callable
import time

from .exceptions import MessyKitchenError
from .context import started_at
from .logging import logger
from .pantry import Food


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
