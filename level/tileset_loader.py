import json
import pygame

from typing import List, Dict, Tuple
from level.tile_type_enum import TileTypeEnum, TileFormatEnum, DecoratorEnum, DecoratorCollisionFormatEnum
from registries.image_registry import ImageRegistery
from registries.collision_registry import CollisionObject, CollisionRect, CollisionSphere
from registries.event_registry import EventRegistry, Event, EventTypeEnum

class DecoratorType():

    def __init__(self, images: List, animation_speed: float, decorator_type: DecoratorEnum, width: int, height: int, center: bool, collision_objects: List[CollisionObject]):
        self.images = []
        for image in images:
            self.images.append(
                ImageRegistery.get_image("media/tileset_image/" + image)
            )

        self.animation_speed = animation_speed
        self.current_animation_time = 0
        self.decorator_type = decorator_type
        self.width = width
        self.height = height
        self.center = center
        self.rendered_images = []
        self.collision_objects = collision_objects

    def update_renders(self, zoom_level: float):
        self.rendered_images = []
        for image in self.images:
            self.rendered_images.append(
                pygame.transform.scale(image, (int(self.width/40 * zoom_level), int(self.height/40 * zoom_level)))
            )

    def render(self, x_pos: float, y_pos: float, zoom_level: float, surface):

        surface_width, surface_height = surface.get_size()

        image_to_render = self.rendered_images[int(self.current_animation_time)]
        if self.center:
            x_offset = 0
            y_offset = 0
            if self.width/40 %2 == 0:
                x_offset = self.width/40/2*zoom_level
            else:
                x_offset = (self.width/40 - 1)/2*zoom_level
            if self.height/40 %2 == 0:
                y_offset = self.height/40/2*zoom_level
            else:
                y_offset = (self.height/40 - 1)/2*zoom_level
            if  (x_pos - x_offset) + self.width/40*zoom_level > 0 and (x_pos - x_offset) < surface_width and\
                 (y_pos - y_offset) + self.height/40*zoom_level > 0 and (y_pos - y_offset) < surface_height:
                surface.blit(image_to_render, (x_pos - x_offset, y_pos - y_offset))
        else:

            surface.blit(image_to_render, (x_pos, y_pos))

    def get_collision_objects(self) -> List[CollisionObject]:
        return self.collision_objects

class TileType():

    complex_format_image_definitions = [
        ([False, False, False, False, True, False, False, False, False], 0, 0, 40, 40), # first row
        ([False, False, False, True, True, False, False, False, False], 40, 0, 40, 40),
        ([False, True, False, False, True, False, False, False, False], 80, 0, 40, 40),
        ([False, False, False, False, True, False, False, True, False], 120, 0, 40, 40),
        ([False, False, False, False, True, True, False, False, False], 160, 0, 40, 40),
        ([False, True, False, False, True, False, False, True, False], 0, 40, 40, 40), # second row
        ([False, False, False, True, True, True, False, False, False], 40, 40, 40, 40),
        ([False, False, False, True, True, False, False, True, False], 80, 40, 40, 40),
        ([False, True, False, False, True, True, False, False, False], 120, 40, 40, 40),
        ([False, True, False, True, True, True, False, False, False], 160, 40, 40, 40),
        ([False, True, False, True, True, False, False, True, False], 0, 80, 40, 40), # third row
        ([False, False, False, True, True, True, False, True, False], 40, 80, 40, 40),
        ([False, True, False, False, True, True, False, True, False], 80, 80, 40, 40),
        ([False, True, False, True, True, True, False, True, False], 120, 80, 40, 40),
        ([True, True, False, True, True, False, False, False, False], 160, 80, 40, 40),
        ([False, True, True, False, True, True, False, False, False], 0, 120, 40, 40), # fourth row
        ([False, False, False, True, True, False, True, True, False], 40, 120, 40, 40),
        ([False, False, False, False, True, True, False, True, True], 80, 120, 40, 40),
        ([False, True, True, False, True, True, False, True, True], 120, 120, 40, 40),
        ([False, False, False, True, True, True, True, True, True], 160, 120, 40, 40),
        ([True, True, False, True, True, False, True, True, False], 0, 160, 40, 40), # fifth row
        ([True, True, True, True, True, True, False, False, False], 40, 160, 40, 40),
        ([True, True, True, True, True, True, False, True, True], 80, 160, 40, 40),
        ([True, True, False, True, True, True, True, True, True], 120, 160, 40, 40),
        ([False, True, True, True, True, True, True, True, True], 160, 160, 40, 40),
        ([True, True, True, True, True, True, True, True, False], 0, 200, 40, 40), # sixth row
        ([False, True, True, True, True, True, True, True, False], 40, 200, 40, 40),
        ([True, True, False, True, True, True, False, True, True], 80, 200, 40, 40),
        ([True, True, False, True, True, True, True, True, False], 120, 200, 40, 40),
        ([False, True, True, True, True, True, False, True, True], 160, 200, 40, 40),
        ([False, True, False, True, True, True, True, True, True], 0, 240, 40, 40), # seventh row
        ([True, True, True, True, True, True, False, True, False], 40, 240, 40, 40),
        ([True, True, False, True, True, False, False, True, False], 80, 240, 40, 40),
        ([False, True, True, True, True, True, False, False, False], 120, 240, 40, 40),
        ([False, True, False, False, True, True, False, True, True], 160, 240, 40, 40),
        ([False, False, False, True, True, True, True, True, False], 0, 280, 40, 40), # eighth row
        ([True, True, False, True, True, True, False, False, False], 40, 280, 40, 40),
        ([False, True, True, False, True, True, False, True, False], 80, 280, 40, 40),
        ([False, False, False, True, True, True, False, True, True], 120, 280, 40, 40),
        ([False, True, False, True, True, False, True, True, False], 160, 280, 40, 40),
        ([True, True, True, True, True, True, True, True, True], 0, 320, 40, 40), # ninth row
        ([False, True, False, True, True, False, False, False, False], 40, 320, 40, 40),
        ([False, False, False, False, True, True, False, True, False], 80, 320, 40, 40),
        #misc patterns
        ([True, True, False, True, True, False, True, True, True], 0, 160, 40, 40),
        ([True, True, True, True, True, False, True, True, False], 0, 160, 40, 40),
        ([False, True, True, False, True, True, True, True, True], 120, 120, 40, 40),
        ([True, True, True, False, True, True, False, True, True], 120, 120, 40, 40),
        ([False, False, True, True, True, True, True, True, True], 160, 120, 40, 40),
        ([True, False, False, True, True, True, True, True, True], 160, 120, 40, 40),
        ([True, True, True, True, True, True, True, False, False], 40, 160, 40, 40),
        ([True, True, True, True, True, True, False, False, True], 40, 160, 40, 40),
        ([False, False, True, True, True, False, True, True, False], 40, 120, 40, 40),
        ([True, False, False, False, True, True, False, True, True], 80, 120, 40, 40),
        ([True, True, False, True, True, False, False, False, True], 160, 80, 40, 40),
        ([False, True, True, False, True, True, True, False, False], 0, 120, 40, 40)
    ]

    def __init__(self, images: List, animation_speed: float, format_in: TileFormatEnum, tile_type: TileTypeEnum, allowed_connections: List[TileTypeEnum]):
        self.images = []
        self.rendered_images = []
        self.rendered_grids = []
        for image in images:
            self.images.append(
                ImageRegistery.get_image("media/tileset_image/" + image)
            )

        self.animation_speed = animation_speed
        self.current_animation_time = 0.0
        self.tile_type = tile_type
        self.format = format_in
        self.allowed_connections = allowed_connections


    def is_tile_type_allowed_for_connection(self, tile_type: TileTypeEnum) -> bool:
        return tile_type in self.allowed_connections


    def update(self, delta: float):
        previous_frame = int(str(self.current_animation_time).split(".")[0])
        self.current_animation_time = self.current_animation_time + self.animation_speed * delta

        if self.current_animation_time >= len(self.images):
            self.current_animation_time = 0.0


    def get_image_positionals_for_surroundings(self, surroundings: List):
        for section in TileType.complex_format_image_definitions:
            if surroundings == section[0]:
                return (section[1], section[2], section[3], section[4])
        
        surroundings[0] = False
        surroundings[2] = False
        surroundings[6] = False
        surroundings[8] = False

        for section in TileType.complex_format_image_definitions:
            if surroundings == section[0]:
                return (section[1], section[2], section[3], section[4])

        return (160, 320, 40, 40)

    def update_renders(self, zoom_level: float):
        for image in self.images:
            if self.format == TileFormatEnum.CONNECTABLE:
                rendered_image = pygame.transform.scale(image, (zoom_level * 5, zoom_level * 9))
            else:
                rendered_image = pygame.transform.scale(image, (zoom_level, zoom_level))
            self.rendered_images.append(rendered_image)


    def render(self, x_pos: float, y_pos: float, width: float, height: float, surface, surroundings: List):
        if self.format == TileFormatEnum.CONNECTABLE:
            positionals = self.get_image_positionals_for_surroundings(surroundings)
            surface.blit(self.rendered_images[int(str(self.current_animation_time).split(".")[0])], (x_pos, y_pos), (positionals[0]/40*width, positionals[1]/40*width, width, height))
        else:
            surface.blit(self.rendered_images[int(str(self.current_animation_time).split(".")[0])], (x_pos, y_pos))


class TileSet():

    def __init__(self, tiles: List[TileType], decorators: List[DecoratorType]):

        identified_types = []

        self.__tiles = {}
        self.__decorators = {}

        for tile in tiles:
            if tile.tile_type in identified_types:
                raise ValueError(str(tile.tile_type) + " already defined in tileset.")
            else:
                identified_types.append(tile)
                self.__tiles[tile.tile_type] = tile

        for decorator in decorators:
            if decorator.decorator_type in identified_types:
                raise ValueError(str(decorator.decorator_type) + " already defined in tileset.")
            else:
                identified_types.append(decorator)
                self.__decorators[decorator.decorator_type] = decorator


    def get_tile_for_type(self, tile_type: TileTypeEnum) -> TileType:
        return self.__tiles[tile_type]

    def get_decorator_for_type(self, decorator_type: DecoratorType):
        return self.__decorators[decorator_type]

    def update_renders(self, zoom_level: int):
        for decorator in self.__decorators.values():
            decorator.update_renders(zoom_level)
        for tile in self.__tiles.values():
            tile.update_renders(zoom_level)

    def update_animations(self, delta: float):
        for tile in self.__tiles.values():
            tile.update(delta)



def load_tileset(tileset_filename: str) -> TileSet:

    with open("media/tileset_data/" + tileset_filename) as tileset_file:
        tileset_data = json.loads(tileset_file.read())

        identified_tiles = []
        identified_decorators = []

        for tile_key, tile_data in tileset_data["tiles"].items():
            tile_enum = TileTypeEnum.get_enum_for_value(tile_key)
            format_enum = TileFormatEnum.get_enum_for_value(tile_data['format'])
            allowed_tiles_for_connections = [tile_enum]
            if "allowed_connections" in tile_data.keys():
                for connection in tile_data["allowed_connections"]:
                    allowed_tiles_for_connections.append(
                        TileTypeEnum.get_enum_for_value(connection)
                    )

            identified_tiles.append(
                TileType(
                    tile_data['images'],
                    tile_data['animated_speed'],
                    format_enum,
                    tile_enum,
                    allowed_tiles_for_connections
                )
            )
        
        for decorator_key, decorator_data in tileset_data["decorators"].items():
            decorator_enum = DecoratorEnum.get_enum_for_value(decorator_key)
            collision_objects = []

            if "collision_objects" in decorator_data.keys():
                for collision_object in decorator_data["collision_objects"]:
                    if collision_object["format"] == DecoratorCollisionFormatEnum.CIRCLE.value:
                        collision_objects.append(
                            CollisionSphere(
                                collision_object["x_pos"],
                                collision_object["y_pos"],
                                collision_object["radius"]
                            )
                        )
                    elif collision_object["format"] == DecoratorCollisionFormatEnum.RECTANGLE.value:
                        collision_objects.append(
                            CollisionRect(
                                collision_object["x_pos"],
                                collision_object["y_pos"],
                                collision_object["width"],
                                collision_object["height"]
                            )
                        )

            identified_decorators.append(
                DecoratorType(
                    decorator_data["images"],
                    decorator_data["animated_speed"],
                    decorator_enum,
                    decorator_data["width"],
                    decorator_data["height"],
                    decorator_data["center_decoration"],
                    collision_objects
                )
            )

        return TileSet(identified_tiles, identified_decorators)
        