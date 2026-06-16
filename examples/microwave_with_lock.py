import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.leftovers import Bulgur, Meatloaf

from kitchenkit.async_prep import microwave


microwave_lock = asyncio.Lock()


async def microwave_meatloaf():
    async with microwave_lock:
        return await microwave(Meatloaf())


async def microwave_bulgur():
    async with microwave_lock:
        return await microwave(Bulgur())


async def main():
    put_on_apron()
    food = await asyncio.gather(
        microwave_meatloaf(),
        microwave_bulgur(),
    )
    serve_food(*food)


if __name__ == "__main__":
    asyncio.run(main())
