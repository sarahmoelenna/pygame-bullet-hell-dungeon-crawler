import pygame
from ui_components.ui_element import UIElement
from registries.image_registry import ImageRegistery

class UIImage(UIElement):

    def __init__(self, file_location: str, x_pos: float, y_pos: float, width: float, height: float):

        self.original_image = ImageRegistery.get_image(file_location)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def resize(self, width: float, height: float):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.original_image, (width, height))

    def move(self, x_change: float, y_change: float):
        self.x_pos = self.x_pos + x_change
        self.y_pos = self.y_pos + y_change
    
    def reposition(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def render(self, surface):
        surface.blit(self.image, (self.x_pos, self.y_pos))