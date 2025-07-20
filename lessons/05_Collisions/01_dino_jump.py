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
        obstacle_height = 40
        obstacle_speed = 5
        obstacle_x = 0

        # Font
        font = pygame.font.SysFont(None, 36)
        score = 0


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        cactus_image = pygame.image.load(images_dir / "cactus_9.png").convert_alpha()
        self.image = pygame.transform.scale(cactus_image, (self.settings.obstacle_width, self.settings.obstacle_height))
        self.rect = self.image.get_rect()
        self.rect.x = Settings.width
        Settings.obstacle_x = Settings.width
        self.rect.y = Settings.height - Settings.obstacle_height
        self.scored = False
        self.explosion = pygame.image.load(images_dir / "explosion1.gif")
        self.alive = True
        self.collided = False

    def update(self):
        self.rect.x -= Settings.obstacle_speed
        Settings.obstacle_x -= Settings.obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.x < 0:
            self.kill()

    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (Settings.obstacle_width, Settings.obstacle_height))
        self.rect = self.image.get_rect(center=self.rect.center)


        


# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self, Settings):
        super().__init__()
        dino_image = pygame.image.load(images_dir / "dino_0.png").convert_alpha()
        self.image = pygame.transform.scale(dino_image, (Settings.size, Settings.size))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = Settings.height - Settings.size - 10

        # Jump variables
        self.velocity = 0
        self.gravity = 1
        self.jump_strength = -15
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity = self.jump_strength
            self.is_jumping = True

        # Apply gravity
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Prevent falling below ground
        if self.rect.bottom >= Settings.height:
            self.rect.bottom = Settings.height
            self.velocity = 0
            self.is_jumping = False


# Create a player object
player = Player(Settings)
player_group = pygame.sprite.Group(player)

# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    
    if random.random() < 0.4:
        obstacle = Obstacle(Settings)
        obstacles.add(obstacle)
        return 1
    return 0

class Game_Over(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        gm_ovr_img = pygame.image.load(images_dir / "game_over_screen.png").convert_alpha()
        self.image = pygame.transform.scale(gm_ovr_img, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

game_over_screen = Game_Over()
game_over_group = pygame.sprite.Group(game_over_screen)
# Main game loop
class Loop(Player, Obstacle):
    def __init__(self, Player, Obstacle):
        self.game_over = False
        self.game_loop( Settings)
    def game_loop(self,Settings):
        clock = pygame.time.Clock()
        last_obstacle_time = pygame.time.get_ticks()

        # Group for obstacles
        obstacles = pygame.sprite.Group()

        obstacle_count = 0

        while not self.game_over:
            # for event in pygame.event.get():
                # if event.type == pygame.QUIT:
                    #pygame.quit()
                    #quit()

            # Update player
            player.update()

            # Add obstacles and update
            if pygame.time.get_ticks() - last_obstacle_time > 500:
                last_obstacle_time = pygame.time.get_ticks()
                obstacle_count += add_obstacle(obstacles)
            obstacles.update()

            # Check for collisions
            
            for obstacle in obstacles:
                if not obstacle.scored and not obstacle.collided and obstacle.rect.right < player.rect.left:
                    Settings.score += 1
                    obstacle.scored = True


            
            collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
            for obstacle in collider:
                if not obstacle.collided:
                    obstacle.collided = True
                    obstacle.explode()
                    self.game_over = True

            # Draw everything
            Settings.screen.fill(Settings.colors['white'])
            player_group.draw(Settings.screen)
            obstacles.draw(Settings.screen)
            
            # Display obstacle count
            obstacle_text = Settings.font.render(f"Obstacles: {obstacle_count}", True, Settings.colors['black'])
            Settings.screen.blit(obstacle_text, (10, 10))

            score_text = Settings.font.render(f"Score: {Settings.score}", True, Settings.colors['black'])
            Settings.screen.blit(score_text, (300, 10))
            pygame.display.update()
            clock.tick(Settings.fps)
        else:
             while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return  # Exit the loop and game

                Settings.screen.fill(Settings.colors['white'])
                game_over_group.draw(Settings.screen)
                pygame.display.update()
                clock.tick(Settings.fps)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.game_over = False
                    game_loop = Loop(Player,Obstacle)
            
        # Game over screen
game_loop = Loop(Player, Obstacle)
