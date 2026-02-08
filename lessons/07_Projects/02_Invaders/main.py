import pygame
from pathlib import Path
d = Path(__file__).parent
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH  = 600
    SCREEN_HEIGHT = 800
    BACKGROUND_SCROLL_SPEED = 2
    FPS = 30
    laser_count = 0

screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
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
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        alien_image = pygame.image.load(d/'images/alien.png').convert_alpha()
        self.image = pygame.transform.scale(alien_image, (25, 25))
        self.rect= self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = pygame.image.load(d/'images/rocket.png').convert_alpha()
        self.image = pygame.transform.scale(player_image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 500
        
player = Player()
player_group = pygame.sprite.Group(player)
alien = Alien()
alien_group = pygame.sprite.Group(alien)

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        laser_image = pygame.image.load(d/'images/projectile.png').convert_alpha()
        self.image = pygame.transform.scale(laser_image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.y = player.rect.y
        self.rect.x = player.rect.x
        self.alive = True
        self.collided = False
    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            Settings.laser_count -= 1
            self.kill()

def shoot_laser(Lasers):
    if Settings.laser_count < 4:
        laser = Laser()
        laser.rect.x = player.rect.x
        Lasers.add(laser)
        Settings.laser_count += 1

def main():
    """Run the main game loop."""
    running = True

    bg = Background()
    all_sprites = pygame.sprite.Group(bg)
    lasers = pygame.sprite.Group()

    clock = pygame.time.Clock()
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_laser(lasers)
        if keys[pygame.K_LEFT]:
            player.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player.rect.x += 5
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        lasers.draw(screen)
        lasers.update()
        pygame.display.flip()
        
        clock.tick(Settings.FPS)
    pygame.quit()



if __name__ == "__main__":
    main()