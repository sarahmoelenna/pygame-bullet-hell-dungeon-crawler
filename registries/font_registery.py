import pygame

class FontRegistery():

    fonts = {}

    @staticmethod
    def get_font(size: int):
        if size in FontRegistery.fonts.keys():
            return FontRegistery.fonts[size]
        else:
            FontRegistery.fonts[size] = pygame.font.SysFont("comicsansms", size)
            return FontRegistery.fonts[size]

