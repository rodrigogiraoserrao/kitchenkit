import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.pantry import Pasta, Rice, Couscous

from kitchenkit.prep import async_cook


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        pasta_task = tg.create_task(async_cook(Pasta()))
        rice_task = tg.create_task(async_cook(Rice()))
        couscous_task = tg.create_task(async_cook(Couscous()))

    pasta = pasta_task.result()
    rice = rice_task.result()
    couscous = couscous_task.result()
    serve_food(pasta, rice, couscous)


if __name__ == "__main__":
    asyncio.run(main())
