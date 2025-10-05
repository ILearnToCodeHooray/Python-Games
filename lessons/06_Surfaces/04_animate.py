import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path

images = Path(__file__).parent / 'images'


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
    frog_direction_vector = pygame.math.Vector2(0, 100)
    frog_position = pygame.math.Vector2(0, 100)
    key_limit = 0
    pygame.math.Vector2(1, 0)
    def draw_frog(frog, index):

        index = index % (len(frog))

        width = frog[0].get_width()
        height = frog[0].get_height()
        composed_image = pygame.Surface((width, height), pygame.SRCALPHA)

        composed_image.blit(frog[index], (0,0))

        return composed_image
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
    
    def move():
        init_position = frog_position

        final_position = frog_position + frog_direction_vector

        length = frog_direction_vector.lenghth()
        N = int(length // 3)
        step = (final_position - frog_position) / N

        for i in range(N):
            frog_position += step
            pygame.draw.line(screen, (255, 0, 0), init_position, final_position, 2)
            pygame.display.flip
    while running:
        key_limit += 1
        screen.fill((0, 0, 139))  # Clear screen with deep blue
        keys = pygame.key.get_pressed()
        # Update animation every few frames
        frame_count += 1
        
        if frame_count % frames_per_image == 0: 
            frog_index = (frog_index + 1) % len(frog_sprites)
            allig_index = (allig_index + 1) % len(allig_sprites)
        
        # Get the current sprite and display it in the middle of the screen
        screen.blit(frog_sprites[frog_index], sprite_rect)
        composed_frog = draw_frog(frog_sprites, frog_index)
        screen.blit(composed_frog, sprite_rect.move(frog_position))
        composed_alligator = draw_alligator(allig_sprites, allig_index)
        screen.blit(composed_alligator,  sprite_rect.move(0, 100))
        screen.blit(log,  sprite_rect.move(0, -100))

        if key_limit%3 == 0:
            if keys[pygame.K_LEFT]:
                frog_direction_vector = frog_direction_vector.rotate(-5)
            elif keys[pygame.K_RIGHT]:
                frog_direction_vector = frog_direction_vector.rotate(5)

        if keys[pygame.K_UP]:
            frog_direction_vector.scale_to_length(frog_direction_vector.length() + 5)
        elif keys[pygame.K_DOWN]:
            frog_direction_vector.scale_to_length(frog_direction_vector.length() - 5)
        elif keys[pygame.K_SPACE]:
            move()
        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
