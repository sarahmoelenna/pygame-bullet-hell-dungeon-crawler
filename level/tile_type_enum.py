from enum import Enum

class TileTypeEnum(Enum):
    BLANK = "BLANK"
    PlainTile = "floor_tile"
    RedTile = "red_tile"
    BlueTile = "blue_tile"
    WALL_TILE = "WALL_TILE"
    STONE_FLOOR = "STONE_FLOOR"
    SNOW_FLOOR = "SNOW_FLOOR"
    STONE_TILE = "STONE_TILE"
    STONE_TILES = "STONE_TILES"
    NEON_TILE = "NEON_TILE"

    def get_enum_for_value(value_in: str):
        for enum in TileTypeEnum:
            if enum.value == value_in:
                return enum
        raise ValueError("Unrecognised Tile Type Enum Value: " + value_in)

class TileFormatEnum(Enum):
    SIMPLE = "SIMPLE"
    CONNECTABLE = "CONNECTABLE"

    def get_enum_for_value(value_in: str):
        for enum in TileFormatEnum:
            if enum.value == value_in:
                return enum
        raise ValueError("Unrecognised Tile Format Enum Value: " + value_in)

class DecoratorEnum(Enum):
    TREE = "TREE"

    def get_enum_for_value(value_in: str):
        for enum in DecoratorEnum:
            if enum.value == value_in:
                return enum
        raise ValueError("Unrecognised Tile Decorator Enum Value: " + value_in)

class DecoratorCollisionFormatEnum(Enum):
    CIRCLE = "CIRCLE"
    RECTANGLE = "RECTANGLE"

    def get_enum_for_value(value_in: str):
        for enum in DecoratorCollisionFormatEnum:
            if enum.value == value_in:
                return enum
        raise ValueError("Unrecognised Tile Decorator Enum Value: " + value_in)