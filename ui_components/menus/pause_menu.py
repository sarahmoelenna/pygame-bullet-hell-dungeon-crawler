from ui_components.ui_set import UISet
from ui_components.clickable_image import ClickableImage
from ui_components.ui_text import UIText
from ui_components.clickable_button import ClickableColouredButton
from state.game_state import GameState
from state.state_enum import StateEnum

class PauseMenu(UISet):

    def __init__(self):

        self.register_ui_element(UIText(600, 400, "Paused", size = 72, center_on_position = True))
        self.register_ui_element(ClickableColouredButton(600, 500, "Resume Game", PauseMenu.change_to_gameplay))
        self.register_ui_element(ClickableColouredButton(600, 600, "Back to Menu", PauseMenu.change_to_main_menu))

    @staticmethod
    def change_to_gameplay():
        print("Changing State to Gameplay")
        GameState.state = StateEnum.GAMEPLAY

    @staticmethod
    def change_to_main_menu():
        print("Changing State to Main Menu")
        GameState.state = StateEnum.MAINMENU
