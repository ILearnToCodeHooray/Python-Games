import pygame
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
    game_over = False

screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Frogger")

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

def main():
    """Run the main game loop."""
    running = True
    bg = Background()
    all_sprites = pygame.sprite.Group(bg)
    clock = pygame.time.Clock()
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
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(Settings.FPS)
    pygame.quit()

if __name__ == "__main__":
    main()