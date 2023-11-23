
import pygame

class Text:
    def __init__(self, font_size, text, color, x, y):
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.color = color
        self.x = x
        self.y = y

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(topleft=(self.x, self.y))
        screen.blit(text_surface, text_rect)
