import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.pantry import Pasta, Rice, Bulgur

from kitchenkit.async_prep import cook


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        pasta_task = tg.create_task(cook(Pasta()))
        rice_task = tg.create_task(cook(Rice()))
        bulgur_task = tg.create_task(cook(Bulgur()))

    pasta = pasta_task.result()
    rice = rice_task.result()
    bulgur = bulgur_task.result()
    serve_food(pasta, rice, bulgur)


if __name__ == "__main__":
    asyncio.run(main())
