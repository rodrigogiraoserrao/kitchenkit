import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.pantry import Asparagus, Broccoli, Carrots, GreenBeans, Leek

from kitchenkit.prep import async_cook, peel_and_slice


peeled = asyncio.Queue()
STOP = object()


async def peeler(foods):
    for food_type in foods:
        done = peel_and_slice(food_type())
        await peeled.put(done)
        await asyncio.sleep(0)


async def cooker(id):
    cooked = []
    print(f"Starting id {id}.")
    while True:
        food = await peeled.get()

        try:
            if food is STOP:
                print(f"{id}: Stopped.")
                return cooked

            print(f"{id}: Got {food.name}.")
            done = await async_cook(food)
            cooked.append(done)
        finally:
            peeled.task_done()


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        cookers = [
            tg.create_task(cooker(1)),
            tg.create_task(cooker(2)),
        ]
        peeler_task = tg.create_task(
            peeler([Asparagus, Broccoli, Carrots, GreenBeans, Leek])
        )

        await peeler_task
        await peeled.join()

        for _ in cookers:
            await peeled.put(STOP)

    cooked = [
        food
        for cooker_task in cookers
        for food in cooker_task.result()
    ]

    serve_food(*cooked)


if __name__ == "__main__":
    asyncio.run(main())
