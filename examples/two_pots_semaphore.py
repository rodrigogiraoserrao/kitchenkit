import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.pantry import Pasta, Rice, Bulgur

from kitchenkit.async_prep import cook


pots_semaphore = asyncio.Semaphore(2)


async def cook_pasta():
    async with pots_semaphore:
        return await cook(Pasta())


async def cook_rice():
    async with pots_semaphore:
        return await cook(Rice())


async def cook_bulgur():
    async with pots_semaphore:
        return await cook(Bulgur())


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        pasta_task = tg.create_task(cook_pasta())
        rice_task = tg.create_task(cook_rice())
        bulgur_task = tg.create_task(cook_bulgur())

    pasta = pasta_task.result()
    rice = rice_task.result()
    bulgur = bulgur_task.result()
    serve_food(pasta, rice, bulgur)


if __name__ == "__main__":
    asyncio.run(main())
