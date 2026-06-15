import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.leftovers import Meatloaf
from kitchenkit.pantry import Avocado, Pasta

from kitchenkit.prep import peel_and_slice
from kitchenkit.async_prep import microwave, cook


async def async_peel_and_slice(food):
    return peel_and_slice(food)


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        pasta_task = tg.create_task(cook(Pasta()))
        meatloaf_task = tg.create_task(microwave(Meatloaf()))
        avocado_task = tg.create_task(async_peel_and_slice(Avocado()))

    pasta = pasta_task.result()
    meatloaf = meatloaf_task.result()
    avocado = avocado_task.result()

    serve_food(pasta, meatloaf, avocado)


if __name__ == "__main__":
    asyncio.run(main())
