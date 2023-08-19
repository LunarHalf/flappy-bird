import pygame
import sys 
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Load fonts and sounds
game_font = pygame.font.Font(None, 40)
flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')

# Game variables
gravity = 0.19
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

# Load images
bg_surface = pygame.image.load('assets/background-night.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_frames = [
    pygame.transform.scale2x(pygame.image.load('assets/bird1.png').convert_alpha()),
    pygame.transform.scale2x(pygame.image.load('assets/bird2.png').convert_alpha()),
    pygame.transform.scale2x(pygame.image.load('assets/bird3.png').convert_alpha())
]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, screen_height // 2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-red.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)
pipe_height = [400, 600, 800]

# Load the game over image
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(screen_width // 2, screen_height // 2))

# Functions
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(screen_width + 100, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(screen_width + 100, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= screen_height - floor_surface.get_height():
        death_sound.play()
        return False

    return True

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > 0]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height - floor_surface.get_height():
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def pipe_score_check():
    global score, can_score

    for pipe in pipe_list:
        if 95 < pipe.centerx < 105 and can_score:
            score += 1
            score_sound.play()
            can_score = False
        if pipe.centerx < 0:
            can_score = True

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, screen_height - floor_surface.get_height()))
    screen.blit(floor_surface, (floor_x_pos + screen_width, screen_height - floor_surface.get_height()))

def update_score(current_score, high_score):
    if current_score > high_score:
        return current_score
    return high_score

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(screen_width // 2, 850))
        screen.blit(high_score_surface, high_score_rect)

# Game loop
# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement -= 12
                    flap_sound.play()
                else:  # Restart the game
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, screen_height // 2)
                    bird_movement = 0
                    score = 0
                    can_score = True

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % len(bird_frames)
            bird_surface = bird_frames[bird_index]
            bird_rect = bird_surface.get_rect(center=bird_rect.center)

    # Update background
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = pygame.transform.rotozoom(bird_surface, -bird_movement * 3, 1)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()

        # Draw the floor
        floor_x_pos -= 1
        draw_floor()  


        # Display score during gameplay
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(score_surface, score_rect)

    else:
        # Display game over screen
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
        draw_floor()

    # Update and display high score
    high_score = max(score, high_score)
    high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(screen_width // 2, 850))
    screen.blit(high_score_surface, high_score_rect)

    # Update the display
    pygame.display.update()
    clock.tick(65)

#End
