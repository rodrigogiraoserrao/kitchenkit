import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.leftovers import Couscous, Meatloaf

from kitchenkit.async_prep import microwave


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        meatloaf_task = tg.create_task(microwave(Meatloaf()))
        couscous_task = tg.create_task(microwave(Couscous()))

    meatloaf = meatloaf_task.result()
    couscous = couscous_task.result()
    serve_food(couscous, meatloaf)


if __name__ == "__main__":
    asyncio.run(main())
