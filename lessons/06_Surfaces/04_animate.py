import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path

images = Path(__file__).parent / 'images'

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.steps_left = 0
        self.position = pygame.math.Vector2(x, y)
        self.direction_vector = pygame.math.Vector2(100, 0)
        self.screen = pygame.display.set_mode((640, 480))
    def draw_line(self, show_line = True):
        end_position = self.position + self.direction_vector
        if show_line:
            pygame.draw.line(self.screen, (255, 0, 0), self.position, end_position, 2)
    def move(self, position):
        self.steps_left = 10
        self.init_position = position

        self.final_position = position + self.direction_vector

        length = self.direction_vector.length()
        N = int(length // 3)
        self.step = (self.final_position - position) / N
    def draw_frog(self, frog, index):

        index = index % (len(frog))

        width = frog[0].get_width()
        height = frog[0].get_height()
        self.composed_image = pygame.Surface((width, height), pygame.SRCALPHA)

        self.composed_image.blit(frog[index], (self.position))
        return self.composed_image

    def update(self):
        if self.steps_left > 0:
            self.position += self.step

            pygame.draw.line(self.screen, (255, 0, 0), self.init_position, self.final_position, 2)

            self.steps_left -= 1
            
def scale_sprites(sprites, scale):
    """Scale a list of sprites by a given factor.

    Args:
        sprites (list): List of pygame.Surface objects.
        scale (int): Scale factor.

    Returns:
        list: List of scaled pygame.Surface objects.
    """
    return [pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale)) for sprite in sprites]
frog = pygame.sprite.Group()
alligator = pygame.sprite.Group()
def main():
    # Initialize Pygame
    pygame.init()
    # Set up the display
    player = Player(0, 0)
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Sprite Animation Test")

    # Load the sprite sheet
    filename = images / 'spritesheet.png'  # Replace with your actual file path
    cellsize = (16, 16)  # Replace with the size of your sprites
    spritesheet = SpriteSheet(filename, cellsize)


    # Load a strip sprites
    frog_sprites = scale_sprites(spritesheet.load_strip(0, 4, colorkey=-1) , 4)
    allig_sprites = scale_sprites(spritesheet.load_strip( (0,4), 7, colorkey=-1), 4)

    # Compose an image
    log = spritesheet.compose_horiz([24, 25, 26], colorkey=-1)
    log = pygame.transform.scale(log, (log.get_width() * 4, log.get_height() * 4))

    # Variables for animation
    frog_index = 0
    allig_index = 0
    frames_per_image = 6
    frame_count = 0

    # Main game loop
    running = True
    sprite_rect = frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    key_limit = 0
    pygame.math.Vector2(1, 0)

    
    def draw_alligator(alligator, index):
        """Creates a composed image of the alligator sprites.

        Args:
            alligator (list): List of alligator sprites.
            index (int): Index value to determine the right side sprite.

        Returns:
            pygame.Surface: Composed image of the alligator.
        """
        
        index = index % (len(alligator)-2)
        
        width = alligator[0].get_width()
        height = alligator[0].get_height()
        composed_image = pygame.Surface((width * 3, height), pygame.SRCALPHA)

        composed_image.blit(alligator[0], (0, 0))
        composed_image.blit(alligator[1], (width, 0))
        composed_image.blit(alligator[(index + 2) % len(alligator)], (width * 2, 0))

        return composed_image
    

    while running:
        key_limit += 1
        keys = pygame.key.get_pressed()
        # Update animation every few frames
        frame_count += 1
        
        if frame_count % frames_per_image == 0: 
            frog_index = (frog_index + 1) % len(frog_sprites)
            allig_index = (allig_index + 1) % len(allig_sprites)
        
        # Get the current sprite and display it in the middle of the screen
        screen.blit(frog_sprites[frog_index], sprite_rect)
        composed_frog = player.draw_frog(frog_sprites, frog_index)
        screen.blit(composed_frog, sprite_rect.move(player.position))
        composed_alligator = draw_alligator(allig_sprites, allig_index)
        screen.blit(composed_alligator,  sprite_rect.move(0, 100))
        screen.blit(log,  sprite_rect.move(0, -100))

        if key_limit%3 == 0:
            if keys[pygame.K_LEFT]:
                player.direction_vector = player.direction_vector.rotate(-5)
            elif keys[pygame.K_RIGHT]:
                player.direction_vector = player.direction_vector.rotate(5)

        if keys[pygame.K_UP]:
            player.direction_vector.scale_to_length(player.direction_vector.length() + 5)
        elif keys[pygame.K_DOWN]:
            player.direction_vector.scale_to_length(player.direction_vector.length() - 5)
        elif keys[pygame.K_SPACE]:
            player.move(player.position)
            
        # Update the display
        player.update()
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 139))  # Clear screen with deep blue
        # Cap the frame rate
        pygame.time.Clock().tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
