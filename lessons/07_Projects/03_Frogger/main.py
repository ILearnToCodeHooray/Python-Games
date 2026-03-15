import pygame
import random
from pathlib import Path
d = Path(__file__).parent
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH  = 600
    SCREEN_HEIGHT = 600
    FPS = 30
    laser_count = 0
    alien_move_speed = 2
    score = 0
    font = pygame.font.SysFont(None, 36)
    colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 255, 0),
            'gray': (127, 127, 127)
        }
    obstacle_width= 100
    obstacle_height = 100
    obstacle_speed = 5
    game_over = False

screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Frogger")

class car_left(pygame.sprite.Sprite):
    def __init__(self, settings, y):
        super().__init__()
        self.settings = settings
        car_image = pygame.image.load(d / "images/carLeft.png").convert_alpha()
        self.image = pygame.transform.scale(car_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.SCREEN_WIDTH
        Settings.obstacle_x = Settings.SCREEN_WIDTH
        self.rect.y = y
        self.scored = False
        self.alive = True
        self.collided = False

    def update(self):
        self.rect.x -= Settings.obstacle_speed
        Settings.obstacle_x -= Settings.obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.x < 0:
            self.kill()

class car_right(pygame.sprite.Sprite):
    def __init__(self, settings, y):
        super().__init__()
        self.settings = settings
        car_image = pygame.image.load(d / "images/carRight.png").convert_alpha()
        self.image = pygame.transform.scale(car_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.SCREEN_WIDTH
        Settings.obstacle_x = 0
        self.rect.y = y
        self.scored = False
        self.alive = True
        self.collided = False

    def update(self):
        self.rect.x -= Settings.obstacle_speed
        Settings.obstacle_x += Settings.obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.x < 0:
            self.kill()
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        orig_image= pygame.image.load(d/'images/frogger_road_bg.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.image.blit(orig_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -50
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = pygame.image.load(d/'images/frog.png').convert_alpha()
        self.image = pygame.transform.scale(player_image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 450

player = Player()
player_group = pygame.sprite.Group(player)

def add_car_left(obstacles, row):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    if row == "row_1":
        y = 375
    if random.random() < 0.4:
        obstacle = car_left(Settings, y)
        obstacles.add(obstacle)
        return 1
    return 0

def add_car_right(obstacles, row):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    if row == "row_2":
        y = 300
    if random.random() < 0.4:
        obstacle = car_right(Settings, y)
        obstacles.add(obstacle)
        return 1
    return 0
def main():
    """Run the main game loop."""
    running = True
    bg = Background()
    all_sprites = pygame.sprite.Group(bg)
    clock = pygame.time.Clock()
    last_car_time = pygame.time.get_ticks()
    row_1 = pygame.sprite.Group()
    row_2 = pygame.sprite.Group()
    car_count = 0
    while running: 
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_UP] and not player.rect.y == 0:
                player.rect.y -= 75
            if keys[pygame.K_DOWN] and not player.rect.y == 450:
                player.rect.y += 75
            if keys[pygame.K_LEFT] and not player.rect.x == 0:
                player.rect.x -= 75
            if keys[pygame.K_RIGHT] and not player.rect.x == 525:
                player.rect.x += 75
        if pygame.time.get_ticks() - last_car_time > 1000:
            last_car_time = pygame.time.get_ticks()
            which_row = random.randint(1,2)
            if which_row == 1:
                car_count += add_car_left(row_1, "row_1")
            elif which_row == 2:
                car_count += add_car_right(row_2, "row_2")
        row_1.update()
        row_2.update()
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        row_1.draw(screen)
        row_2.draw(screen)
        pygame.display.flip()
        clock.tick(Settings.FPS)
    pygame.quit()

if __name__ == "__main__":
    main()