import pygame
import random
import math
from pathlib import Path
d = Path(__file__).parent/ 'images'
pygame.init()

class Colors:
    """Constants for Colors"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (255, 255, 255)

class Settings:
    """Settings for the game"""
    font = pygame.font.SysFont(None, 36)
    colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 255)}
    width: int = 600
    height: int = 400
    gravity: float = 0.3
    player_start_x: int = 100
    player_start_y: int = 100
    player_v_y: float = 0  # Initial y velocity
    player_v_x: float = 0  # Initial x velocity
    player_width: int = 20
    player_height: int = 20
    player_jump_velocity: float = 15
    frame_rate: int = 15
    lives = 3
    move = pygame.Vector2(0, 1)
    fuel = 100
    score = 0

class Game:
    """Main object for the top level of the game. Holds the main loop and other
    update, drawing and collision methods that operate on multiple other
    objects, like the player and obstacles."""

    def __init__(self, settings: Settings):
        pygame.init()

        self.settings = settings
        self.running = True

        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.clock = pygame.time.Clock()

        # Turn Gravity into a vector
        self.gravity = pygame.Vector2(0, self.settings.gravity)
        self.v1_tup = (0,270)
        self.v2_tup = (10, 350)
        self.v3_tup = (50, 340)
        self.v4_tup = (150, 280)
        self.v5_tup = (200, 330)
        self.v6_tup = (230, 330)
        self.v7_tup = (280, 380)
        self.v8_tup = (330, 380)
        self.v9_tup = (400, 300)
        self.v10_tup = (420, 320)
        self.v11_tup = (470, 320)
        self.v12_tup = (530, 270)
        self.v13_tup = (600, 270)

        # All terrain points in order. Built once here instead of being
        # re-wrapped in new Vector2 objects every frame inside run().
        self.terrain_points = [
            self.v1_tup, self.v2_tup, self.v3_tup, self.v4_tup, self.v5_tup,
            self.v6_tup, self.v7_tup, self.v8_tup, self.v9_tup, self.v10_tup,
            self.v11_tup, self.v12_tup, self.v13_tup,
        ]

        # Landing pads: touching one of these while descending slowly is a
        # safe landing worth points. These are checked before the crash walls
        # below so that a shared endpoint (e.g. v5, which is shared between
        # the v4-v5 wall and the v5-v6 pad) resolves as a landing rather than
        # a crash - this matches the priority order of the original code.
        self.landing_pads = [
            (self.v5_tup, self.v6_tup, 5),
            (self.v7_tup, self.v8_tup, 2),
            (self.v10_tup, self.v11_tup, 2),
            (self.v12_tup, self.v13_tup, 1),
        ]

        # Every other terrain segment ends the game on contact.
        pad_segments = {(pad[0], pad[1]) for pad in self.landing_pads}
        self.crash_walls = [
            (a, b) for a, b in zip(self.terrain_points, self.terrain_points[1:])
            if (a, b) not in pad_segments
        ]

    def run(self):
        """Main game loop"""
        player = Player(self)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            if Settings.fuel == 0:
                self.running = False
            player.update()

            self.screen.fill(Colors.BACKGROUND_COLOR)
            player.draw(self.screen)
            fuel_text = Settings.font.render(f"Fuel: {(Settings.fuel)}", True, Settings.colors['black'])
            self.screen.blit(fuel_text, (10, 10))
            score_text = Settings.font.render(f"Score: {(Settings.score)}", True, Settings.colors['black'])
            self.screen.blit(score_text, (150, 10))
            lives_text = Settings.font.render(f"Lives: {(Settings.lives)}", True, Settings.colors['black'])
            self.screen.blit(lives_text, (300, 10))

            # Draw the terrain by walking the same point list used for
            # collision, instead of manually re-listing every segment.
            for start, end in zip(self.terrain_points, self.terrain_points[1:]):
                pygame.draw.line(self.screen, Settings.colors['black'], start, end, 2)

            if Settings.lives == 0:
                self.running = False
            pygame.display.flip()
            self.clock.tick(self.settings.frame_rate)
        pygame.quit()

class Player(pygame.sprite.Sprite):
    """Player class, just a bouncing rectangle"""

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        settings = self.game.settings
        self.original_image = pygame.image.load(d/'lander.png')
        self.original_image_scaled = pygame.transform.scale(self.original_image, (self.original_image.get_width() / 2, self.original_image.get_height() / 2))
        self.image = self.original_image_scaled.copy()
        self.width = settings.player_width
        self.height = settings.player_height
        self.angle = 0
        self.rect = self.original_image_scaled.get_rect()
        # Vector for our jump velocity, which is just up
        self.v_jump = pygame.Vector2(0, -settings.player_jump_velocity)

        # Player position
        self.pos = pygame.Vector2(settings.player_start_x,
                                  settings.player_start_y if settings.player_start_y is not None else settings.height - self.height)

        # Player's velocity
        self.vel = pygame.Vector2(settings.player_v_x, settings.player_v_y)  # Velocity vector
        #self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def going_up(self):
        """Check if the player is going up"""
        return self.vel.y < 0

    def going_down(self):
        """Check if the player is going down"""
        return self.vel.y > 0

    def going_left(self):
        """Check if the player is going left"""
        return self.vel.x < 0

    def going_right(self):
        """Check if the player is going right"""
        return self.vel.x > 0

    def at_top(self):
        """Check if the player is at the top of the screen"""
        return self.pos.y <= 0

    def at_bottom(self):
        """Check if the player is at the bottom of the screen"""
        return self.pos.y >= self.game.settings.height - self.height

    def at_left(self):
        """Check if the player is at the left of the screen"""
        return self.pos.x <= 0

    def at_right(self):
        """Check if the player is at the right of the screen"""
        return self.pos.x >= self.game.settings.width - self.width

    def update(self):
        """Update player position, continuously jumping"""
        self.update_v()
        self.update_pos()

    def _reset_to_start(self):
        """Send the player back to the starting position with zero velocity."""
        self.pos.x = self.game.settings.player_start_x
        self.pos.y = self.game.settings.player_start_y
        self.vel.y = 0
        self.vel.x = 0

    def _handle_terrain_collision(self):
        """Check the player's rect against every terrain segment.

        Landing on a pad while descending slowly (vel.y < 6 and not stationary)
        awards points and resets the player. Touching any other segment ends
        the game. Returns True if a collision was handled, so the caller can
        skip the at_top() bounce check for this frame (matching the original
        if/elif priority).
        """
        for start, end, score in self.game.landing_pads:
            if self.rect.clipline(start, end) and self.vel.y < 6 and self.vel.y != 0:
                Settings.score += score
                self._reset_to_start()
                return True

        for start, end in self.game.crash_walls:
            if self.rect.clipline(start, end):
                self.game.running = False
                return True

        return False

    def update_v(self):
        """Update the player's velocity based on gravity and bounce on edges"""
        self.vel += self.game.gravity  # Add gravity to the velocity
        self.rect.y = self.pos.y
        self.rect.x = self.pos.x
        if self.at_bottom() and self.going_down():
            if self.vel.y < 6 and self.vel.y != 0.3:
                Settings.score += 1
                self._reset_to_start()
            elif self.vel.y > 6:
                Settings.lives -= 1
                self._reset_to_start()
            elif self.vel.x > 6:
                Settings.lives -= 1
                self._reset_to_start()
            self.vel.y = 0
            self.vel.x = 0

        collided = self._handle_terrain_collision()
        if not collided and self.at_top() and self.going_up():
            self.vel.y = 0

            # If the player hits one side of the screen or the other, bounce the
            # player. we are also checking if the player has a velocity going farther
            # off the screeen, because we don't want to bounce the player if it's
            # already going away from the edge
        if self.at_bottom():
            drag = (0, 0)
        else:
            drag = -self.vel * 0.1
            self.vel += drag

    def update_pos(self):
        """Update the player's position based on velocity"""
        self.pos += self.vel  # Update the player's position based on the current velocity

        # If the player is at the bottom, stop the player from falling and
        # stop the jump

        if self.at_bottom():
            self.pos.y = self.game.settings.height - self.height

        if self.at_top():
            self.pos.y = 0

        # Don't let the player go off the left side of the screen
        if self.at_left():
            self.pos.x = self.game.settings.width - self.width

        # Don't let the player go off the right side of the screen
        elif self.at_right():
            self.pos.x = 0

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.angle += 5
            Settings.move = pygame.Vector2(0,1)
            Settings.move.rotate_ip(-self.angle)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.angle -= 5
            Settings.move = pygame.Vector2(0,1)
            Settings.move.rotate_ip(-self.angle)
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.vel -= Settings.move
            Settings.fuel -= 1

    def draw(self, screen):
        self.image_rotated = pygame.transform.rotate(self.image, self.angle)
        screen.blit(self.image_rotated, (self.pos.x, self.pos.y))
settings = Settings()
game = Game(settings)
game.run()