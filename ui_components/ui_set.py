from ui_components.ui_element import UIElement
from interface.mouse import Mouse
from ui_components.clickable_ui_element import ClickableUIElement

class UISet(UIElement):

    
        
    def register_ui_element(self, ui_element: UIElement):
        if not hasattr(self, "ui_element_registry"):
            self.ui_element_registry = []

        self.ui_element_registry.append(ui_element)

    def render(self, screen):
        for item in self.ui_element_registry:
            item.render(screen)

    def update(self, mouse: Mouse):
        for item in self.ui_element_registry:
            if isinstance(item, ClickableUIElement):
                if item.is_mouse_state_applicable(mouse):
                    item.apply_mouse_effect(mouse)