__author__ = 'hammy'

from food_common import enum_type

@enum_type
class Flavor:
    SWEET = 0x0001
    SALTY = 0x0002
    SAVORY = 0x0004
    SOUR = 0x0008
    BITTER = 0x0010
    UMAMI = 0x0020
    HEARTY = 0x0040


@enum_type
class IngredientUse:
    REQUIRED = 0
    OPTIONAL = 1
    SWAPPABLE = 2


class Food:
    def __init__(self):
        suffix = '%sness'
        grammerer = '%si'
        tastes = lambda f: (f if f[-1] != 'Y' else grammerer % f[:-1]).lower()
        flavorings = {suffix % tastes(flavor): 0 for flavor in Flavor.enum_keys}
        self.__dict__ = dict(self.__dict__, **flavorings)
        self.__dict__.update()


if __name__ == '__main__':
    food = Food()
    print food.__dict__
    print food.savoriness
