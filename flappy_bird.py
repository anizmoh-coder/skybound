import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_POWER = -15
PIPE_SPEED = 5
PIPE_GAP = 150
PIPE_WIDTH = 80
PIPE_SPAWN_DISTANCE = 150

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
YELLOW = (255, 200, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Skybound - Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.radius = 15
        self.velocity = 0
    
    def jump(self):
        self.velocity = JUMP_POWER
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius)
        # Draw eye
        pygame.draw.circle(surface, BLACK, (int(self.x) + 5, int(self.y) - 5), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        pipe_height = random.randint(50, SCREEN_HEIGHT - 100)
        self.top = pipe_height - PIPE_GAP
        self.bottom = pipe_height
        self.passed = False
    
    def update(self):
        self.x -= PIPE_SPEED
    
    def draw(self, surface):
        # Top pipe
        pygame.draw.rect(surface, GREEN, (self.x, 0, self.width, self.top))
        pygame.draw.rect(surface, BLACK, (self.x - 2, self.top - 5, self.width + 4, 10))
        
        # Bottom pipe
        pygame.draw.rect(surface, GREEN, (self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom))
        pygame.draw.rect(surface, BLACK, (self.x - 2, self.bottom - 5, self.width + 4, 10))
    
    def is_offscreen(self):
        return self.x + self.width < 0
    
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom)
        return top_rect, bottom_rect

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_counter = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.bird.jump()
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.bird.update()
        
        # Spawn pipes
        self.pipe_counter += 1
        if self.pipe_counter > PIPE_SPAWN_DISTANCE:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.pipe_counter = 0
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
            # Check if bird passed the pipe
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
        
        # Remove offscreen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_offscreen()]
        
        # Collision detection
        self.check_collisions()
        
        # Check boundaries
        if self.bird.y - self.bird.radius < 0 or self.bird.y + self.bird.radius > SCREEN_HEIGHT:
            self.game_over = True
    
    def check_collisions(self):
        bird_rect = self.bird.get_rect()
        
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                self.game_over = True
    
    def draw(self):
        screen.fill(BLUE)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(screen)
        
        # Draw bird
        self.bird.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
            screen.blit(final_score_text, 
                       (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        
        pygame.display.flip()
    
    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_counter = 0

def main():
    game = Game()
    running = True
    
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
