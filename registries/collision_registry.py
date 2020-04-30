from typing import Dict, List
from uuid import uuid4
import pygame

class CollisionObject():

        def __init__(self):
            sekf.id = str(uuid4())

        def has_collidied(self, object_to_check: 'CollisionObject') -> bool:
            raise NotImplementedError("has_collidied must be implemented")

class CollisionRect(CollisionObject):

    def __init__(self, x_pos: float, y_pos: float, width: float, height: float):
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.width = float(width)
        self.height = float(height)

    def has_collidied(self, object_to_check: CollisionObject) -> bool:
        pass

class CollisionSphere(CollisionObject):

    def __init__(self, x_pos: float, y_pos: float, radius: float):
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.radius = float(radius)

    def has_collidied(self, object_to_check: CollisionObject) -> bool:
        pass

class CollisionPoint(CollisionObject):

    def __init__(self, x_pos: float, y_pos: float):
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)

    def has_collidied(self, object_to_check: CollisionObject) -> bool:
        return False

class Collidable():

    def get_collision_object() -> CollisionObject:
        raise NotImplementedError("get_collision_object must be implemented")

class CollisionRegistry():

    current_instance = None

    @staticmethod
    def get_instance() -> 'CollisionRegistry':
        if CollisionRegistry.current_instance is None:
            CollisionRegistry.current_instance = CollisionRegistry()
        return CollisionRegistry.current_instance

    @staticmethod
    def destroy():
        CollisionRegistry.current_instance = None

    def __init__(self):
        self.collision_objects = {}

    def register_grid(self, collision_grid: Dict):
        grid_uuid = str(uuid4())
        print(len(collision_grid.keys()))
        for x in range(collision_grid["width"]):
            for y in range(collision_grid["height"]):
                if collision_grid[x][y] == 1:
                    self.collision_objects[grid_uuid] = [CollisionRect(x, y, 1, 1)]

    
    def register_decorators(self, decorations: List['Decoration']):
        for decoration in decorations:
            if decoration.out_of_bounds == False:
                self.collision_objects[decoration.id] = decoration.get_collision_objects()

    def render(self, zoom_level: int, surface):
        for collision_objects in self.collision_objects.values():
            for collision_object in collision_objects:
                if isinstance(collision_object, CollisionRect):
                    pygame.draw.rect(surface, (255,255,0), (collision_object.x_pos * zoom_level, collision_object.y_pos * zoom_level, collision_object.width * zoom_level, collision_object.height * zoom_level))
                elif isinstance(collision_object, CollisionSphere):
                    pygame.draw.circle(surface, (255,255,0), (collision_object.x_pos * zoom_level, collision_object.y_pos * zoom_level), collision_object.radius * zoom_level)
