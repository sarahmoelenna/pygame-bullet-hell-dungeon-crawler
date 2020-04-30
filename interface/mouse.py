import pygame
from typing import Tuple

class Mouse():

    def __init__(self, x_pos: float, y_pos: float, is_clicked: bool, previous_x_pos: float, previous_y_pos: float, previous_is_clicked: bool):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.is_clicked = is_clicked
        self.previous_x_pos = previous_x_pos
        self.previous_y_pos = previous_y_pos
        self.previous_is_clicked = previous_is_clicked

    def get_movement_change(self) -> Tuple[float, float]:
        return self.x_pos - self.previous_x_pos, self.y_pos - self.previous_y_pos

    def has_clicked_state_changed(self):
        if self.is_clicked == self.previous_is_clicked:
            return False
        return True

def get_mouse(previous_mouse: Mouse) -> Mouse:

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    if previous_mouse:
        return Mouse(mouse_x, mouse_y, mouse_clicked, previous_mouse.x_pos, previous_mouse.y_pos, previous_mouse.is_clicked)
    else: 
        return Mouse(mouse_x, mouse_y, mouse_clicked, 0, 0, False)