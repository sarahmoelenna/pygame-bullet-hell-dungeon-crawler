import pygame

class KeyState():

    def __init__(self, is_pressed: bool, has_pressed_state_changed: bool):
        self.is_pressed = is_pressed
        self.has_pressed_state_changed = has_pressed_state_changed


class KeyBoard():

    old_state = None
    current_state = None

    def __init__(self):
        KeyBoard.key_state = pygame.key.get_pressed()
        KeyBoard.old_state = KeyBoard.key_state

    @staticmethod
    def update():
        KeyBoard.old_state = KeyBoard.key_state
        KeyBoard.key_state = pygame.key.get_pressed()
        

    @staticmethod
    def get_key_state(key) -> KeyState:
        return KeyState(
            KeyBoard.key_state[key],
            KeyBoard.key_state[key] == KeyBoard.old_state[key]
        )