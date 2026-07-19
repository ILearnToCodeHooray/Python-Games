import pygame
import math
from pathlib import Path
import random
import numpy
pygame.init()
assets = Path(__file__).parent / "images"

class Settings:
    """Class to store game configuration.""" 
    font = pygame.font.SysFont(None, 36)
    width = 600
    height = 600
    fps = 60
    triangle_size = 20
    projectile_speed = 5 
    projectile_size = 11
    shoot_delay = 250  # 250 milliseconds between shots, or 4 shots per second
    colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 255)}
    score = 0
    lives = 3

class Tank(pygame.sprite.Sprite):
    """Class representing the spaceship."""

    def __init__(self, settings, position):
        super().__init__()

        self.game = None  # will be set in Game.add()
        self.settings = settings

        self.angle = 0
        self.original_image = self.create_spaceship_image()

        self.velocity = pygame.Vector2(0, 0)

        self.acceleration = 1
        # For Sprites, the image and rect attributes are part of the Sprite class
        # and are important. The image is the surface that will be drawn on the screen
        spaceship_position = position
        self.image = self.original_image.copy() 
        self.rect = self.image.get_rect(center=position)

        # These values help us limit the rate of fire
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = self.settings.shoot_delay  

    def create_spaceship_image(self):
        """Creates the spaceship shape as a surface."""
        image = pygame.Surface( (self.settings.triangle_size * 2, self.settings.triangle_size * 2),pygame.SRCALPHA)
        points = [
            (self.settings.triangle_size, 0),  # top point
            (0, self.settings.triangle_size * 2),  # left side point
            (self.settings.triangle_size * 2,self.settings.triangle_size * 2, ),  # right side point
        ]
        pygame.draw.polygon(image, self.settings.colors["white"], points)
        return image
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.angle -= 5

        if keys[pygame.K_RIGHT]:
            self.angle += 5

        if keys[pygame.K_SPACE] and self.ready_to_shoot():
            self.fire_projectile()
        if keys[pygame.K_UP]:
            self.velocity = (pygame.Vector2(0, -1).rotate(self.angle))*self.acceleration
            if self.acceleration < 4:
                self.acceleration = self.acceleration * 1.03
        else:
            self.acceleration = 0.9
            self.velocity = self.velocity*self.acceleration
        if keys[pygame.K_LSHIFT]:
            self.rect.center = (random.randint(0, 600), random.randint(0, 600))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        # Reassigning the rect because the image has changed.
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.rect.center += self.velocity

        screen_width = self.settings.width
        screen_height = self.settings.height

        if self.rect.right < 0:
            self.rect.x = screen_width
            
        if self.rect.left > screen_width:
            self.rect.x = 0

        if self.rect.top > screen_height:
            self.rect.y = 0

        if self.rect.bottom < 0:
            self.rect.y = screen_height
        # Dont forget this part! If you don't call the Sprite update method, the
        # sprite will not be drawn
        super().update()

tanks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Game:
    """Class to manage the game loop and objects."""

    def __init__(self, settings):
        pygame.init()
        pygame.key.set_repeat(1250, 1250)
        self.side = random.randint(1,4)
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))

        pygame.display.set_caption("Really Boring Asteroids")

        self.clock = pygame.time.Clock()
        self.running = True

    def add(self, sprite):
        """Adds a sprite to the game. Really important! This group is used to
        update and draw all of the sprites."""

        sprite.game = self

        all_sprites.add(sprite)

        if isinstance(sprite, Tank):
            tanks.add(sprite)


    def run(self):
        """Main Loop for the game."""
        
       
        while True:
            while self.running:
                self.clock.tick(self.settings.fps)

            pygame.quit()

if __name__ == "__main__":

    settings = Settings()

    game = Game(settings)

    tank = Tank(
        settings, position=(settings.width // 2, settings.height // 2)
    )
    game.add(tank)

    game.run()
