import pygame

from registries.font_registery import FontRegistery
from ui_components.ui_element import UIElement
from typing import Tuple

class UIText(UIElement):

    def __init__(self, x_pos: float, y_pos: float, text: str, size: int = 30, center_on_position: bool = False, colour: Tuple = (0,0,0,)):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.colour = colour
        self.center_on_position = center_on_position
        self.size = size

    def get_size(self) -> Tuple[float, float]:
        return FontRegistery.get_font(self.size).size(self.text)
    
    def render(self, screen):

        text_surface = FontRegistery.get_font(self.size).render(self.text, True, self.colour)
        if self.center_on_position:
            est_width, est_height = FontRegistery.get_font(self.size).size(self.text)
            screen.blit(text_surface, (self.x_pos - est_width/2, self.y_pos - est_height/2))
        else:
            screen.blit(text_surface, (self.x_pos, self.y_pos))