# Import and initialize the pygame library
import pygame
from datetime import datetime
pygame.init()

from ui_components.menus.main_menu import MainMenu
from ui_components.menus.gameplay_ui import GameplayUI
from ui_components.menus.pause_menu import PauseMenu
from interface.mouse import get_mouse
from interface.keyboard import KeyBoard
from state.game_state import GameState
from state.state_enum import StateEnum
from level.grid import Grid
from ui_components.ui_text import UIText
from registries.event_registry import EventRegistry

class Game():

    main_menu = MainMenu()
    gamplay = GameplayUI()
    pause_menu = PauseMenu()
    KeyBoard()
    my_grid = Grid(300,200,"test_tileset.json")

    fps_text = UIText(10,10, "fps: ", 30, False, (0,0,0))
    
    def __init__(self):

        info = pygame.display.Info()

        self.game_objects = []
        #self.screen = pygame.display.set_mode([info.current_w, info.current_h], pygame.NOFRAME)
        self.screen = pygame.display.set_mode([1200, 800])
        

    def render(self):

        self.screen.fill((10, 10, 120))

        Game.my_grid.render(self.screen)

        if GameState.state == StateEnum.MAINMENU:
            Game.main_menu.render(self.screen)
        elif GameState.state == StateEnum.GAMEPLAY:
            Game.gamplay.render(self.screen)
        elif GameState.state == StateEnum.PAUSED:
            Game.pause_menu.render(self.screen)


        Game.fps_text.render(self.screen)
        

        # Flip the display
        pygame.display.flip()

    def main_loop(self):
        # Run until the user asks to quit
        running = True
        mouse = get_mouse(None)
        previous_time = datetime.now()

        while running:
            current_time = datetime.now()
            delta = (current_time - previous_time).total_seconds()
            if delta == 0:
                delta = 0.001
            Game.fps_text.text = "FPS: " + str(int(60/delta))

            EventRegistry.process_subscriptions(delta)

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            mouse = get_mouse(mouse)
            KeyBoard.update()

            if GameState.state == StateEnum.MAINMENU:
                Game.main_menu.update(mouse)
            elif GameState.state == StateEnum.GAMEPLAY:
                Game.gamplay.update(mouse)
            elif GameState.state == StateEnum.PAUSED:
                Game.pause_menu.update(mouse)

            Game.my_grid.update(mouse, delta)

            if KeyBoard.get_key_state(pygame.K_RETURN).is_pressed and KeyBoard.get_key_state(pygame.K_RETURN).has_pressed_state_changed:
                Game.my_grid = Grid(300,200,"test_tileset.json")

            EventRegistry.purge_events()
            self.render()

            previous_time = current_time
        # Done! Time to quit.
        pygame.quit()



game = Game()
game.main_loop()