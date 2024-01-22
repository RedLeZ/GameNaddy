import os
import sys
import pygame
import random
import time
from button import Button
from text import Text
from jsonReader import LoadJson, UpdateJson
from pygame.math import Vector2


class Projectile:
    def __init__(
        self, x, y, size, images_folder, target_x, target_y, player_rect, speed
    ):
        self.rect = pygame.Rect(x, y, size, size)
        self.images_folder = images_folder
        self.images = self.load_images(size)
        self.image = random.choice(self.images)
        self.speed = speed
        self.target_x = target_x
        self.target_y = target_y
        self.player_rect = player_rect

    def load_images(self, size):
        image_files = [f for f in os.listdir(self.images_folder) if f.endswith(".png")]
        images = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.images_folder, f)), (size, size)
            )
            for f in image_files
        ]
        return images

    def move_towards_player(self):
        if not self.rect.colliderect(self.player_rect):
            self.calculate_direction()
            self.rect.x += int(round(self.speed * self.direction.x))
            self.rect.y += int(round(self.speed * self.direction.y))

    def calculate_direction(self):
        target_position = Vector2(self.target_x, self.target_y)
        self_position = Vector2(self.rect.x, self.rect.y)
        if self_position != target_position:
            self.direction = target_position - self_position
            self.direction.normalize_ip()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


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
                quit()
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
        self.title = Text(48, "Select Level", (255, 255, 255), 200, 100)
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
                quit()
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
        self.max_score_text = Text(
            48, f"Max Score: {self.load_max_score()}", (255, 255, 255), 200, 350
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
                quit()
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
        self.max_score_text.draw(screen)
        self.restart_button.draw(screen)
        self.back_to_menu_button.draw(screen)

    def load_max_score(self):
        data = LoadJson("data.json")
        return data["MaxScore"]


class GameState:
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.screen_shake_intensity = 20
        self.screen_shake_duration = 0.5
        self.screen_shake_timer = 0
        self.clock = pygame.time.Clock()
        self.score_text = Text(36, f"Score: {self.score}", (255, 255, 255), 10, 10)

        pygame.mixer.init()
        self.pop_sound = pygame.mixer.Sound("pop.mp3")
        background_image_path = "Image.png"
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_image = pygame.transform.scale(
            self.background_image, (self.game.width, self.game.height)
        )
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1)

        self.target_width = 50
        self.target_height = 50
        self.target_x = (self.game.width - self.target_width) // 2
        self.target_y = (self.game.height - self.target_height) // 2
        self.original_player_position = (self.target_x, self.target_y)
        self.player_position = self.original_player_position
        self.isHurt = False
        self.player_image = pygame.image.load("player.png").convert_alpha()
        self.player_image = pygame.transform.scale(
            self.player_image, (self.target_width, self.target_height)
        )

        self.projectile_size = 50
        self.projectiles = []
        self.projectile_speed = 1
        self.last_projectile_spawn_time = time.time()

        self.hearts = 100
        self.heart_size = 30
        self.heart_image = pygame.image.load("hrt.png").convert_alpha()
        self.heart_image = pygame.transform.scale(
            self.heart_image, (self.heart_size, self.heart_size)
        )
        self.hearts_images = [
            pygame.Rect(
                10 + i * (self.heart_size + 5), 50, self.heart_size, self.heart_size
            )
            for i in range(self.hearts)
        ]

        self.wave_duration = 30
        self.wave_timer = time.time()
        self.wave_number = 1

        self.player = pygame.Rect(
            self.target_x, self.target_y, self.target_width, self.target_height
        )

        self.player_vulnerability_cooldown = 0.145
        self.player_last_hit_time = 0
        self.player_vulnerable = True
        self.hurt_sound = pygame.mixer.Sound("hurt.mp3")

        self.restricted_zone_size = 300
        self.restricted_zone_color = (0, 0, 0, 128)
        self.restricted_zone = pygame.Rect(
            (self.game.width - self.restricted_zone_size) // 2,
            (self.game.height - self.restricted_zone_size) // 2,
            self.restricted_zone_size,
            self.restricted_zone_size,
        )


        
    def load_max_score(self):
        data = LoadJson("data.json")
        return data["MaxScore"]
    
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
        current_time = time.time()

        if current_time - self.wave_timer > self.wave_duration:
            self.start_new_wave()

        if current_time - self.last_projectile_spawn_time > 5:
            self.last_projectile_spawn_time = current_time

            for _ in range(3):
                projectile_x = random.randint(0, self.game.width - self.projectile_size)
                projectile_y = random.randint(
                    0, self.game.height - self.projectile_size
                )

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
                    "images/",
                    self.target_x + self.target_width / 2,
                    self.target_y + self.target_height / 2,
                    self.player,
                    self.projectile_speed,
                )
                self.projectiles.append(projectile)

        for projectile in self.projectiles:
            projectile.move_towards_player()

            if projectile.rect.colliderect(self.player) and self.player_vulnerable:
                self.player_vulnerable = False
                self.player_last_hit_time = time.time()

                if self.hearts > 0:
                    self.hearts -= 1

                    self.hurt_sound.play()

                self.projectiles.remove(projectile)

                if self.hearts == 0:
                    self.game_over()

        if (
            not self.player_vulnerable
            and time.time() - self.player_last_hit_time
            > self.player_vulnerability_cooldown
        ):
            self.player_vulnerable = True

        self.score_text.text = f"Score: {self.score}"

        self.draw(self.game.screen)

    def draw(self, screen):
        pygame.draw.rect(screen, self.restricted_zone_color, self.restricted_zone)
        screen.blit(self.background_image, (0, 0))

        screen.blit(self.player_image, self.player.topleft)

        for projectile in self.projectiles:
            projectile.draw(screen)

        self.score_text.draw(screen)

        for heart_rect in self.hearts_images[: self.hearts]:
            screen.blit(self.heart_image, heart_rect.topleft)

        wave_text = Text(
            36, f"Wave: {self.wave_number}", (255, 255, 255), self.game.width - 150, 10
        )
        wave_text.draw(screen)

        self.player.topleft = self.original_player_position

    def start_new_wave(self):
        self.wave_number += 1
        self.wave_timer = time.time()
        self.projectile_size -= 1
        self.projectile_speed += 0.3

    def game_over(self):
        new_state = RestartState(self.game)
        self.game.set_state(new_state)
        max_score = self.load_max_score()
        if self.score > max_score:
            self.maxScore = self.score
            UpdateJson("data.json", "MaxScore", self.score)
        else:
            pass

        pygame.mixer.music.stop()
