import asyncio

from kitchenkit import put_on_apron, serve_food
from kitchenkit.pantry import Asparagus, Broccoli, Carrots, GreenBeans, Leek

from kitchenkit.async_prep import peel_and_slice, cook


peeled = asyncio.Queue()
STOP = object()


async def producer(foods):
      for food_type in foods:
          done = await peel_and_slice(food_type())
          await peeled.put(done)
          await asyncio.sleep(0)


async def consumer(id):
    cooked = []
    print(f"Starting id {id}.")
    while True:
        food = await peeled.get()

        try:
            if food is STOP:
                print(f"{id}: Stopped.")
                return cooked

            print(f"{id}: Got {food.name}.")
            done = await cook(food)
            cooked.append(done)
        finally:
            peeled.task_done()


async def main():
    put_on_apron()

    async with asyncio.TaskGroup() as tg:
        consumers = [
            tg.create_task(consumer(1)),
            tg.create_task(consumer(2)),
        ]
        producer_task = tg.create_task(
      producer([Asparagus, Broccoli, Carrots, GreenBeans, Leek])
  )

        await producer_task
        await peeled.join()

        for _ in consumers:
            peeled.put(STOP)

        cooked = [
            food
            for consumer_task in consumers
            for food in consumer_task.result()
        ]

    serve_food(*cooked)


if __name__ == "__main__":
    asyncio.run(main())
