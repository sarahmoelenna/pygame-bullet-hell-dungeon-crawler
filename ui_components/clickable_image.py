from ui_components.ui_image import UIImage
from ui_components.clickable_ui_element import ClickableUIElement
from interface.mouse import Mouse

class ClickableImage(UIImage, ClickableUIElement):

    def is_mouse_state_applicable(self, mouse: Mouse):
        if self.x_pos <= mouse.x_pos and self.x_pos + self.width >= mouse.x_pos and self.y_pos <= mouse.y_pos and \
             self.y_pos + self.height >= mouse.y_pos and mouse.is_clicked == True and mouse.has_clicked_state_changed() == True:
            return True
        return False
    
    def apply_mouse_effect(self, mouse: Mouse):
        self.move(15, 15)