import pygame
from pathlib import Path
d = Path(__file__).parent
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH  = 600
    SCREEN_HEIGHT = 750
    FPS = 30
    laser_count = 0
    alien_move_speed = 2
    score = 0
    font = pygame.font.SysFont(None, 36)
    colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'blue': (0, 0, 255)
        }
    game_over = False

screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Frogger")

class Background(pygame.sprite.Sprite):
    def __init__(self, colors, tile_width=100, scroll_speed=120):
        super().__init__()
        self.tile_width = tile_width
        self.scroll_speed = scroll_speed  # pixels per second
        self.image = self.make_repeating_pattern(colors)
        self.rect = self.image.get_rect(topleft=(0, 0))  # where pattern starts
        self.pattern_width = self.image.get_width()

    def make_color_tile(self, color):
        """Return a 100px-wide Surface as tall as the screen, filled with color."""
        surf = pygame.Surface((self.tile_width, Settings.SCREEN_HEIGHT))
        surf.fill(color)
        return surf

    def make_repeating_pattern(self, colors):
        """Create one long repeating strip of colored tiles."""
        pattern_w = self.tile_width * len(colors)
        pattern = pygame.Surface((pattern_w, Settings.SCREEN_HEIGHT)).convert()
        x = 0
        for color in colors:
            pattern.blit(self.make_color_tile(color), (x, 0))
            x += self.tile_width
        return pattern
    
    def update(self):
        """Update the position of the background."""
        
        self.rect.x -= Settings.BACKGROUND_SCROLL_SPEED
        
        if self.rect.right <= Settings.SCREEN_WIDTH:
            self.rect.x = 0

def main():
    """Run the main game loop."""
    running = True


    bg = Background()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bg)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        
        clock.tick(Settings.FPS)

    pygame.quit()
