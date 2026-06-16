import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.pantry import Pasta, Rice, Couscous

from kitchenkit.async_prep import cook


pots_semaphore = asyncio.Semaphore(2)


async def cook_pasta():
    async with pots_semaphore:
        return await cook(Pasta())


async def cook_rice():
    async with pots_semaphore:
        return await cook(Rice())


async def cook_couscous():
    async with pots_semaphore:
        return await cook(Couscous())


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        pasta_task = tg.create_task(cook_pasta())
        rice_task = tg.create_task(cook_rice())
        Couscous_task = tg.create_task(cook_couscous())

    pasta = pasta_task.result()
    rice = rice_task.result()
    couscous = Couscous_task.result()
    serve_food(pasta, rice, couscous)


if __name__ == "__main__":
    asyncio.run(main())
