import pygame
import ball

BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        drawpaddle = pygame.draw.rect(self.image, color, [0, 0, width, height])
        drawpaddle
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:

            self.rect.y = 400

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 15:
            self.rect.x = 20

    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x > 80:
            self.rect.x = 80
            """
           Definitioner för att spelaren inte ska kunna röra sig ut från spel skärmen
           """
