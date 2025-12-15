
# shishkebab.py
# Pygame Zero game (Flappy-style). Run with: pgzrun shishkebab.py

import random
from pygame import Rect
from pgzero.actor import Actor
from pgzero.keyboard import keys  # for key constants in on_key_down

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

# Astronaut setup
astronaut = Actor('astronaut')  # ensure images/astronaut.png exists
astronaut.pos = (75, HEIGHT // 2)
velocity = 0

# Input flags (we'll set these via on_key_down)
wants_jump = False
wants_reset = False

# Pipes setup
pipes = []


def _create_pipe_pair(x_start: int):
    """Create a top/bottom pipe Rect pair starting at x_start."""
    top_height = random.randint(100, 400)
    return {
        'top': Rect((x_start, 0), (70, top_height)),
        'bottom': Rect((x_start, top_height + gap), (70, HEIGHT - top_height - gap))
    }


# Initialize a few pipes off-screen to the right
for i in range(3):
    pipes.append(_create_pipe_pair(WIDTH + i * 200))


def reset_game():
    """Reset all game state to start a new round."""
    global velocity, score, game_over, pipes, wants_jump, wants_reset
    astronaut.pos = (75, HEIGHT // 2)
    velocity = 0
    score = 0
    game_over = False
    wants_jump = False
    wants_reset = False
    pipes = []
    for i in range(3):
        pipes.append(_create_pipe_pair(WIDTH + i * 200))


def draw():
    """
    Pygame Zero draw() hook.
    'screen' is injected by Pygame Zero; no import needed.
    """
    screen.clear()
    screen.blit('background', (0, 0))  # ensure images/background.png exists

    astronaut.draw()

    for pipe in pipes:
        screen.draw.filled_rect(pipe['top'], 'green')
        screen.draw.filled_rect(pipe['bottom'], 'green')

    screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")

    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=60, color="red")
        screen.draw.text("Press SPACE or UP to restart",
                         center=(WIDTH // 2, HEIGHT // 2 + 50),
                         fontsize=28, color="white")


def update():
    """
    Pygame Zero update() hook.
    """
    global velocity, game_over, score, wants_jump, wants_reset

    # Apply queued input (set in on_key_down)
    if not game_over and wants_jump:
        velocity = jump_strength
        wants_jump = False  # consume jump
    elif game_over and wants_reset:
        reset_game()
        return

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
            score += 1
            pipes.append(_create_pipe_pair(WIDTH))

        # Collision detection
        astronaut_rect = Rect(
            (astronaut.x - astronaut.width // 2, astronaut.y - astronaut.height // 2),
            (astronaut.width, astronaut.height)
        )

        for pipe in pipes:
            if (astronaut_rect.colliderect(pipe['top']) or
                    astronaut_rect.colliderect(pipe['bottom'])):
                game_over = True
                break

        # Check bounds
        if astronaut.y > HEIGHT or astronaut.y < 0:
            game_over = True


def on_key_down(key):
    """
    Called by Pygame Zero when a key is pressed.
    We avoid using 'keyboard.space' in update() to sidestep the error you saw.
    """
    global wants_jump, wants_reset
    if key in (keys.SPACE, keys.UP):
        # If game is running, this triggers a jump.
        # If game_over, this triggers a reset.
        if game_over:
            wants_reset = True
        else:
            wants_jump = True
# End of shishkebab.py