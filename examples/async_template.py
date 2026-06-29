import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.leftovers import Meatloaf
from kitchenkit.pantry import Avocado, Pasta

from kitchenkit.prep import async_microwave, async_cook, peel_and_slice


async def async_peel_and_slice(food):
    return peel_and_slice(food)


async def main():
    put_on_apron()

    food = await asyncio.gather(
        async_cook(Pasta()),
        async_microwave(Meatloaf()),
        async_peel_and_slice(Avocado())
    )

    serve_food(*food)


if __name__ == "__main__":
    asyncio.run(main())
