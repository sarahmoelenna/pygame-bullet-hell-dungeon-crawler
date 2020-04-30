import pygame
from level.tileset_loader import load_tileset
from level.tile_type_enum import TileTypeEnum, DecoratorEnum
from random import randrange
from interface.mouse import Mouse
from interface.keyboard import KeyBoard
from level.grid_generator_helper import MazeGenerator
from registries.collision_registry import CollisionRegistry
from typing import List
from threading import Thread

class Grid():

    current_tileset = None

    def __init__(self, width: int, height: int, tileset_filename: str):

        if width % 4 != 0 or height % 4 != 0:
            raise ValueError("grid dimensions must be multiple of four. provided: " + str(width) + " " + str(height))

        self.x_pos = 0
        self.y_pos = 0

        Grid.current_tileset = load_tileset(tileset_filename)

        self.tileset_filename = tileset_filename
        self.zoom_level = 20
        
        generator = MazeGenerator(width, height, Grid.current_tileset)
        self.grid, collision_grid, self.decorations = generator.generate_grid()
        self.width = self.grid["width"]
        self.height = self.grid["height"]
        self.grid_render = None
        self.decoration_render = None
        Grid.current_tileset.update_renders(self.zoom_level)
        
        collision = CollisionRegistry.get_instance()
        collision.register_grid(collision_grid)
        collision.register_decorators(self.decorations)
        
    
    def update(self, mouse: Mouse, delta: float):
        Grid.current_tileset.update_animations(delta)

        if KeyBoard.get_key_state(pygame.K_w).is_pressed:
            self.y_pos = self.y_pos + 200 * delta
        if KeyBoard.get_key_state(pygame.K_s).is_pressed:
            self.y_pos = self.y_pos - 200 * delta

        if KeyBoard.get_key_state(pygame.K_a).is_pressed:
            self.x_pos = self.x_pos + 200 * delta
        if KeyBoard.get_key_state(pygame.K_d).is_pressed:
            self.x_pos = self.x_pos - 200 * delta

    
    def random_grid(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                random_number = randrange(0, 3)
                if random_number == 0:
                    self.grid[x][y] = Grid.current_tileset.get_tile_for_type(TileTypeEnum.PlainTile)
                elif random_number == 1:
                    self.grid[x][y] = Grid.current_tileset.get_tile_for_type(TileTypeEnum.RedTile)
                else:
                    self.grid[x][y] = Grid.current_tileset.get_tile_for_type(TileTypeEnum.BlueTile)

    
    def render(self, screen):
        
        screen_width, screen_height = screen.get_size()

        for x in range(0, self.width):
            for y in range(0, self.height):
                if (x + 1) * self.zoom_level - self.x_pos >= 0 and x * self.zoom_level - self.x_pos <= screen_width and\
                     (y + 1) * self.zoom_level - self.y_pos >= 0 and y * self.zoom_level - self.y_pos <= screen_height:

                    surroundings = [
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x-1][y-1].tile_type) if x - 1 >= 0 and y - 1 >= 0 else True,
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x][y-1].tile_type) if y - 1 >= 0 else True,
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x+1][y-1].tile_type) if x + 1 < self.grid["width"] and y - 1 >= 0 else True,
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x-1][y].tile_type) if x - 1 >= 0 else True,
                        True,
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x+1][y].tile_type) if x + 1 < self.grid["width"] else True,
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x-1][y+1].tile_type) if x - 1 >= 0 and y + 1 < self.grid["height"]  else True,
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x][y+1].tile_type) if y + 1 < self.grid["height"] else True,
                        self.grid[x][y].is_tile_type_allowed_for_connection(self.grid[x+1][y+1].tile_type) if x + 1 < self.grid["width"] and y + 1 < self.grid["height"] else True,
                    ]

                    self.grid[x][y].render(x * self.zoom_level - self.x_pos, y * self.zoom_level - self.y_pos, self.zoom_level, self.zoom_level, screen, surroundings)
        
        for decoration in self.decorations:
            decoration.render(self.x_pos, self.y_pos, self.zoom_level, screen)

        collision = CollisionRegistry.get_instance()
        collision.render(self.zoom_level, screen)

        for decoration in self.decorations:
            decoration.render(self.x_pos, self.y_pos, self.zoom_level, screen)

        collision = CollisionRegistry.get_instance()
        collision.render(self.zoom_level, screen)



    