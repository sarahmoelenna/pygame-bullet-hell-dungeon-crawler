from ui_components.ui_set import UISet
from ui_components.clickable_image import ClickableImage
from ui_components.ui_text import UIText
from ui_components.clickable_button import ClickableColouredButton
from state.game_state import GameState
from state.state_enum import StateEnum

class MainMenu(UISet):

    def __init__(self):

        #self.register_ui_element(ClickableImage("./media/picture.jpg", 0, 0, 120, 120))
        self.register_ui_element(UIText(600, 400, "MAIN MENU", size = 72, center_on_position = True))
        self.register_ui_element(ClickableColouredButton(600, 500, "Start Game", MainMenu.change_to_gameplay))

    @staticmethod
    def change_to_gameplay():
        print("Changing State to Gameplay")
        GameState.state = StateEnum.GAMEPLAY
