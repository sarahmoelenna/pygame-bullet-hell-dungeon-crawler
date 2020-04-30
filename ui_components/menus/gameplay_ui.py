from ui_components.ui_set import UISet
from ui_components.ui_text import UIText
from ui_components.clickable_button import ClickableColouredButton
from state.game_state import GameState
from state.state_enum import StateEnum

class GameplayUI(UISet):

    def __init__(self):

        self.register_ui_element(UIText(600, 400, "LEVEL", size = 72, center_on_position = True))
        self.register_ui_element(ClickableColouredButton(600, 500, "Pause", GameplayUI.change_to_pause))

    @staticmethod
    def change_to_pause():
        print("Changing State to Paused")
        GameState.state = StateEnum.PAUSED
