import pygame

class ImageRegistery():

    images = {}

    @staticmethod
    def get_image(file_location: int):
        if file_location in ImageRegistery.images.keys():
            return ImageRegistery.images[file_location]
        else:
            ImageRegistery.images[file_location] = pygame.image.load(file_location)
            return ImageRegistery.images[file_location]