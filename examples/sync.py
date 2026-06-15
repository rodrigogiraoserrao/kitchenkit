from kitchenkit import put_on_apron, serve_food
from kitchenkit.leftovers import Meatloaf
from kitchenkit.pantry import Avocado, Pasta

from kitchenkit.prep import peel_and_slice, microwave, cook


def main():
    put_on_apron()
    avocado = peel_and_slice(Avocado())
    pasta = cook(Pasta())
    meatloaf = microwave(Meatloaf())
    serve_food(pasta, meatloaf, avocado)


if __name__ == "__main__":
    main()
