import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.leftovers import Bulgur, Meatloaf
from kitchenkit.async_prep import microwave


async def main():
    put_on_apron()
    food = await asyncio.gather(
        microwave(Meatloaf()),
        microwave(Bulgur()),
    )
    serve_food(*food)


if __name__ == "__main__":
    asyncio.run(main())
