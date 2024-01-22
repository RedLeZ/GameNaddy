import pygame
from game_states import MenuState


# Pixabay
# thanks to Lesiakower
class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("DEFENDE YASSINE")

        self.current_state = MenuState(self)

    def set_state(self, new_state):
        self.current_state = new_state

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            events = pygame.event.get()

            self.current_state.handle_events(events)
            self.current_state.update()

            self.current_state.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)


game_instance = Game(600, 400)


game_instance.run()
