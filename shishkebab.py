
import random
from sense_hat import SenseHat
from pygame.rect import Rect
from pgzero.actor import Actor  # Import Actor for Pygame Zero
from pgzero.builtins import screen  # Import screen for Pygame Zero
# 'screen' is provided by Pygame Zero automatically when running with pgzrun

# Pygame Zero config
WIDTH = 400
HEIGHT = 600

# Game variables
gap = 150
pipe_speed = 2
gravity = 0.3
jump_strength = -6
score = 0
game_over = False

# Sense HAT
sense = SenseHat()

# Astronaut setup (Actor and Rect are provided by Pygame Zero when run via pgzrun)
astronaut = Actor('astronaut')  # ensure images/astronaut.png exists
astronaut.pos = (75, HEIGHT // 2)
velocity = 0

# Pipes setup
pipes = []

def _create_pipe_pair(x_start):
    top_height = random.randint(100, 400)
    return {
        'top': Rect((x_start, 0), (70, top_height)),
        'bottom': Rect((x_start, top_height + gap), (70, HEIGHT - top_height - gap))
    }

for i in range(3):
    pipes.append(_create_pipe_pair(WIDTH + i * 200))


def reset_game():
    global velocity, score, game_over, pipes
    astronaut.pos = (75, HEIGHT // 2)
    velocity = 0
    score = 0
    game_over = False
    pipes = []
    for i in range(3):
        pipes.append(_create_pipe_pair(WIDTH + i * 200))


def draw():
    screen.clear()
    screen.blit('background', (0, 0))  # ensure images/background.png exists
    astronaut.draw()
    for pipe in pipes:
        screen.draw.filled_rect(pipe['top'], 'green')
        screen.draw.filled_rect(pipe['bottom'], 'green')
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        screen.draw.text("Press joystick to restart", center=(WIDTH//2, HEIGHT//2+50), fontsize=28, color="white")


def update():
    global velocity, game_over, score

    # ---------------- Sense HAT joystick input ----------------
    # Use 'up' or 'middle' press to flap / restart
    for e in sense.stick.get_events():
        if e.pressed:
            if not game_over and e.direction in ('up', 'middle'):
                velocity = jump_strength
            elif game_over and e.direction in ('up', 'middle'):
                reset_game()

    if not game_over:
        # Gravity & movement
        velocity += gravity
        astronaut.y += velocity

        # Move pipes
        for pipe in pipes:
            pipe['top'].x -= pipe_speed
            pipe['bottom'].x -= pipe_speed

        # Add new pipes and remove old ones
        if pipes and pipes[0]['top'].x < -70:
            pipes.pop(0)
            # when a pipe leaves the screen, count a point and add a new pipe
            score += 1
            pipes.append(_create_pipe_pair(WIDTH))

        # Collision detection
        astronaut_rect = Rect(
            (astronaut.x - astronaut.width//2, astronaut.y - astronaut.height//2),
            (astronaut.width, astronaut.height)
        )
        for pipe in pipes:
            if astronaut_rect.colliderect(pipe['top']) or astronaut_rect.colliderect(pipe['bottom']):
                game_over = True
                break

        # Check bounds
        if astronaut.y > HEIGHT or astronaut.y < 0:
            game_over = True

