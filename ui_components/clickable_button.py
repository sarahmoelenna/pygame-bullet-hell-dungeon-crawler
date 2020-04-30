from ui_components.clickable_ui_element import ClickableUIElement
from ui_components.ui_text import UIText
from ui_components.ui_element import UIElement
from typing import Tuple, Callable
from interface.mouse import Mouse
import pygame

class ClickableColouredButton(ClickableUIElement, UIElement):

    def __init__(self, x_pos: float, y_pos: float, text: str, callback: Callable, background_colour: Tuple[float, float, float] = (255,255,255,)):

        self.text = UIText(x_pos, y_pos, text, size = 30, center_on_position = True)
        self.background_colour = background_colour
        self.width, self.height = self.text.get_size()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.callback = callback

    def is_mouse_state_applicable(self,  mouse: Mouse):
        if self.x_pos - self.width/2 <= mouse.x_pos and self.x_pos - self.width/2 + self.width >= mouse.x_pos and self.y_pos - self.height/2 <= mouse.y_pos and \
             self.y_pos - self.height/2 + self.height >= mouse.y_pos and mouse.is_clicked == True and mouse.has_clicked_state_changed() == True:
            return True
        return False

    def apply_mouse_effect(self,  mouse: Mouse):
        self.callback()

    def render(self, surface):
        pygame.draw.rect(surface, self.background_colour, (self.x_pos - self.width/2, self.y_pos - self.height/2, self.width, self.height))

        self.text.render(surface)

    