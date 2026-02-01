import pygame
from pathlib import Path
d = Path(__file__).parent
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    BACKGROUND_SCROLL_SPEED = 2
    FPS = 30
    
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
print(pygame.display.get_window_size())
pygame.display.set_caption("Space Invaders")

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        orig_image= pygame.image.load(d/'images/space.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.image.blit(orig_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = -200

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = pygame.image.load(d/'images/rocket.png').convert_alpha()
        self.image = pygame.transform.scale(player_image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 500
def main():
    """Run the main game loop."""
    running = True


    bg = Background()
    player = Player()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group.add(player)
    all_sprites.add(bg)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= 10
                if event.key == pygame.K_RIGHT:
                    player.rect.x += 10
            if event.type == pygame.QUIT:
                running = False


        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        
        clock.tick(Settings.FPS)
    pygame.quit()



if __name__ == "__main__":
    main()