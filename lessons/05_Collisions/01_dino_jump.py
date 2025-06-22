"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
class Settings:
        width = 600
        height = 300
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Dino Jump")

        # Colors
        colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'blue': (0, 0, 255)
        }

        # FPS
        fps = 60

        # Player attributes
        size = 25

        speed = 5

        # Obstacle attributes
        obstacle_width= 20
        obstacle_height = 20
        obstacle_speed = 5

        # Font
        font = pygame.font.SysFont(None, 36)


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.image = pygame.Surface((self.settings.obstacle_width, self.settings.obstacle_height))
        self.image.fill(self.settings.colors['black'])
        self.rect = self.image.get_rect()
        self.rect.x = self.width
        self.rect.y = self.height - self.obstacle_height - 10

        self.explosion = pygame.image.load(images_dir / "explosion1.gif")

    def update(self):
        self.rect.x -= self.obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()

    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (self.obstacle_width, self.obstacle_height))
        self.rect = self.image.get_rect(center=self.rect.center)


# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.image = pygame.Surface((self.settings.size, self.settings.size))
        self.image.fill(self.settings.colors['blue'])
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = self.settings.height - self.settings.size - 10
        self.settings.speed = self.settings.speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep the player on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height

# Create a player object
player = Player(Settings)
player_group = pygame.sprite.GroupSingle(player)

# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    if random.random() < 0.4:
        obstacle = Obstacle()
        obstacles.add(obstacle)
        return 1
    return 0


# Main game loop
class Loop(pygame.sprite.Sprite, Settings):
    def game_loop():
        clock = pygame.time.Clock()
        game_over = False
        last_obstacle_time = pygame.time.get_ticks()

        # Group for obstacles
        obstacles = pygame.sprite.Group()

        player = Player()

        obstacle_count = 0

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Update player
            player.update()

            # Add obstacles and update
            if pygame.time.get_ticks() - last_obstacle_time > 500:
                last_obstacle_time = pygame.time.get_ticks()
                obstacle_count += add_obstacle(self.obstacles)
            
            self.obstacles.update()

            # Check for collisions
            collider = pygame.sprite.spritecollide(player, self.obstacles, dokill=False)
            if collider:
                collider[0].explode()
        
            # Draw everything
            self.screen.fill(self.settings.colors['white'])
            pygame.draw.rect(self.screen, self.settings.colors['blue'], player)
            self.obstacles.draw(self.screen)

            # Display obstacle count
            obstacle_text = self.font.render(f"Obstacles: {obstacle_count}", True, self.settings.colors['black'])
            self.screen.blit(obstacle_text, (10, 10))

            pygame.display.update()
            self.clock.tick(self.fps)

        # Game over screen
        self.screen.fill(self.setings.colors['white'])

if __name__ == "__main__":
    game_loop()
