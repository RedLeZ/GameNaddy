# game_states.py
from importlib_metadata import Prepared
import pygame
import random
import time
from button import Button
from text import Text
import sys
from pygame.math import Vector2


#don't mind him
pygame.mixer.init()
class Projectile:
    def __init__(self, x, y, size, color, target_x, target_y, player_rect, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed = speed
        self.target_x = target_x
        self.target_y = target_y
        self.player_rect = player_rect  # Pass the player's rect as an argument

    def move_towards_player(self):
        if not self.rect.colliderect(
            self.player_rect
        ):  # Check if not already colliding with the player
            self.calculate_direction()
            self.rect.x += int(round(self.speed * self.direction.x))
            self.rect.y += int(round(self.speed * self.direction.y))

    def calculate_direction(self):
        target_position = Vector2(self.target_x, self.target_y)
        self_position = Vector2(self.rect.x, self.rect.y)

        # Check if the projectile is not at the same position as the player
        if self_position != target_position:
            self.direction = target_position - self_position
            self.direction.normalize_ip()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class MenuState:
    def __init__(self, game):
        self.game = game
        self.title = Text(48, "Defend By Force", (255, 255, 255), 180, 100)
        self.start_button = Button(
            200,
            200,
            200,
            50,
            (0, 128, 255),
            "Start Game",
            (255, 255, 255),
            self.start_game,
        )

    def start_game(self):
        self.game.set_state(LevelsState(self.game))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_mouse_over():
                    self.start_button.perform_action()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.title.draw(screen)
        self.start_button.draw(screen)


class LevelsState:
    def __init__(self, game):
        self.game = game
        self.title = Text(48, "Levels State", (255, 255, 255), 200, 100)
        self.endless_button = Button(
            200,
            200,
            200,
            50,
            (0, 128, 255),
            "Endless Mode",
            (255, 255, 255),
            self.start_endless_mode,
        )

    def start_endless_mode(self):
        new_state = GameState(self.game)
        self.game.set_state(new_state)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.endless_button.is_mouse_over():
                    self.endless_button.perform_action()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.title.draw(screen)
        self.endless_button.draw(screen)


class RestartState:
    def __init__(self, game):
        self.game = game
        self.title = Text(48, "Game Over", (255, 255, 255), 200, 100)
        self.restart_button = Button(
            200,
            200,
            200,
            50,
            (0, 128, 255),
            "Restart",
            (255, 255, 255),
            self.restart_game,
        )
        self.back_to_menu_button = Button(
            200,
            270,
            240,
            50,
            (0, 128, 255),
            "Back to Main Menu",
            (255, 255, 255),
            self.back_to_menu,
        )

    def restart_game(self):
        new_state = GameState(self.game)
        self.game.set_state(new_state)

    def back_to_menu(self):
        new_state = MenuState(self.game)
        self.game.set_state(new_state)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.is_mouse_over():
                    self.restart_button.perform_action()
                elif self.back_to_menu_button.is_mouse_over():
                    self.back_to_menu_button.perform_action()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.title.draw(screen)
        self.restart_button.draw(screen)
        self.back_to_menu_button.draw(screen)


class GameState:
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.score_text = Text(36, f"Score: {self.score}", (255, 255, 255), 10, 10)
        self.pop_sound = pygame.mixer.Sound("pop.mp3")
        background_image_path = "Image.png"
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_image = pygame.transform.scale(
            self.background_image, (self.game.width, self.game.height)
        )
        # Rectangle (target) properties
        self.target_width = 50
        self.target_height = 50
        self.target_color = (0, 255, 0)
        self.target_x = (self.game.width - self.target_width) // 2
        self.target_y = (self.game.height - self.target_height) // 2

        # Projectiles properties
        self.projectile_size = 50
        self.projectile_color = (0, 255, 0)
        self.projectiles = []
        self.projectile_speed = 1
        self.last_projectile_spawn_time = time.time()
        # Hearts properties
        self.hearts = 3
        self.heart_size = 30
        self.heart_image = pygame.image.load("hrt.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (self.heart_size, self.heart_size))
        self.hearts_images = [
            pygame.Rect(
                10 + i * (self.heart_size + 5), 50, self.heart_size, self.heart_size
            )
            for i in range(self.hearts)
        ]

        # Wave system properties
        self.wave_duration = 30  # Wave duration in seconds
        self.wave_timer = time.time()
        self.wave_number = 1

        # Player properties
        self.player = pygame.Rect(
            self.target_x, self.target_y, self.target_width, self.target_height
        )

        # Player vulnerability cooldown
        self.player_vulnerability_cooldown = 0.145
        self.player_last_hit_time = 0
        self.player_vulnerable = True

        # Restricted zone properties
        self.restricted_zone_size = 300
        self.restricted_zone_color = (0, 0, 0, 128)
        self.restricted_zone = pygame.Rect(
            (self.game.width - self.restricted_zone_size) // 2,
            (self.game.height - self.restricted_zone_size) // 2,
            self.restricted_zone_size,
            self.restricted_zone_size,
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_projectiles = [
                    projectile
                    for projectile in self.projectiles
                    if projectile.rect.collidepoint(mouse_pos)
                ]

                for projectile in clicked_projectiles:
                    self.projectiles.remove(projectile)
                    self.score += 1
                    self.pop_sound.play()

    def update(self):
        # Update wave system
        current_time = time.time()
        if current_time - self.wave_timer > self.wave_duration:
            self.start_new_wave()

        # Spawn projectiles periodically outside the restricted zone
        if current_time - self.last_projectile_spawn_time > 5:  # Spawn every 5 seconds
            self.last_projectile_spawn_time = current_time  # Update last spawn time

            for _ in range(3):  # Spawn 3 projectiles
                projectile_x = random.randint(0, self.game.width - self.projectile_size)
                projectile_y = random.randint(
                    0, self.game.height - self.projectile_size
                )

                # Ensure the projectile is outside the restricted zone
                while self.restricted_zone.colliderect(
                    pygame.Rect(
                        projectile_x,
                        projectile_y,
                        self.projectile_size,
                        self.projectile_size,
                    )
                ):
                    projectile_x = random.randint(
                        0, self.game.width - self.projectile_size
                    )
                    projectile_y = random.randint(
                        0, self.game.height - self.projectile_size
                    )

                projectile = Projectile(
                    projectile_x,
                    projectile_y,
                    self.projectile_size,
                    self.projectile_color,
                    self.target_x + self.target_width / 2,
                    self.target_y + self.target_height / 2,
                    self.player,
                    self.projectile_speed,
                )
                self.projectiles.append(projectile)

        # Update projectiles
        for projectile in self.projectiles:
            projectile.move_towards_player()

            # Check if projectile touches the player
            if projectile.rect.colliderect(self.player) and self.player_vulnerable:
                self.player_vulnerable = False
                self.player_last_hit_time = time.time()

                if self.hearts > 0:
                    self.hearts -= 1

                self.projectiles.remove(projectile)

                if self.hearts == 0:
                    self.game_over()

        # Check player vulnerability cooldown
        if (
            not self.player_vulnerable
            and time.time() - self.player_last_hit_time
            > self.player_vulnerability_cooldown
        ):
            self.player_vulnerable = True

        # Update score text
        self.score_text.text = f"Score: {self.score}"

    def draw(self, screen):
        pygame.draw.rect(screen, self.restricted_zone_color, self.restricted_zone)
        screen.blit(self.background_image, (0, 0))

        

        pygame.draw.rect(screen, self.target_color, self.player)

        for projectile in self.projectiles:
            projectile.draw(screen)

        self.score_text.draw(screen)

        for heart_rect in self.hearts_images[: self.hearts]:
            screen.blit(self.heart_image, heart_rect.topleft)

        wave_text = Text(
            36, f"Wave: {self.wave_number}", (255, 255, 255), self.game.width - 150, 10
        )
        wave_text.draw(screen)

    def start_new_wave(self):
        self.wave_number += 1
        self.wave_timer = time.time()
        self.projectile_size -= 1
        self.projectile_speed += 0.3

    def game_over(self):
        new_state = RestartState(self.game)
        self.game.set_state(new_state)
