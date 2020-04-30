from interface.mouse import Mouse

class ClickableUIElement():

    def is_mouse_state_applicable(self, mouse: Mouse):
        raise NotImplementedError("is_mouse_state_applicable function must be implemented")

    def apply_mouse_effect(self, mouse: Mouse):
        raise NotImplementedError("apply_mouse_effect function must be implemented")