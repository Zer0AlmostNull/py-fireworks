import os
# hide watermark
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from random import randrange
from particles import *
from vector2 import *

WND_WIDTH, WND_HEIGHT = 1920, 1080
FPS = 60

def get_random_firework():
    BOTTOM_PADDING = 10
   
    # life span is equal to distance they travel divided by -velocity.y
    VELOCITY = -10
    MAX_LIFESPAN = (WND_HEIGHT * 0.75) / -VELOCITY

    return Firework(
                    position = Vector2(randint(0, WND_WIDTH), WND_HEIGHT - randint(0, BOTTOM_PADDING)),
                    color = (randint(0, 255), randint(0, 255), randint(0, 255)),
                    velocity = Vector2(0, VELOCITY),
                    size = Vector2(10, 30),
                    lifetime = randint(MAX_LIFESPAN//2, MAX_LIFESPAN),)

def main():
    # Initialize Pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((WND_WIDTH, WND_HEIGHT))
    pygame.display.set_caption("Fireworks")
    clock = pygame.time.Clock()
    
    # Particle settings
    MAX_FIREWORKS = 3
    particles = [get_random_firework() for _ in range(MAX_FIREWORKS)]
    firework_count = MAX_FIREWORKS

    # Run the game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update particles
        for p in particles[:]:
            if bool(p.update()):
                # firework explosion
                if isinstance(p, Firework):
                    MAX_VEL = 15
                    COUNT = 20
                    particles += [ExplosionParticle(
                                    position = p.position,
                                    color = p.color,
                                    lighten_colors = (100,100,100),
                                    size = Vector2(20, 2),
                                    velocity = Vector2(randint(-MAX_VEL, MAX_VEL), randint(-MAX_VEL, 0)),
                                    lifetime = 30,
                                    wobbling = Vector2(0,0),
                                    explosion_level = 1
                                    ) 
                                for _ in range(COUNT)]
                    firework_count -= 1
                # particle explosion
                elif isinstance(p, ExplosionParticle):
                    # spawn even move particles
                    if p.explosion_level>0:
                        MAX_VEL = 10
                        COLOR_R = 40
                        COUNT = 5
                        particles += [ExplosionParticle(
                                    position = p.position,
                                    color = p.color,
                                    lighten_colors = (100 + randint(-COLOR_R,COLOR_R), 100+randint(-COLOR_R,COLOR_R), 100+randint(-COLOR_R,COLOR_R)),
                                    size = Vector2(20, 2),
                                    velocity = Vector2(randint(-MAX_VEL, MAX_VEL), randint(-MAX_VEL, 0)),
                                    lifetime = 30,
                                    wobbling = Vector2(0,0),
                                    explosion_level = p.explosion_level
                                    ) 
                                for _ in range(COUNT)]
                
                # remove particle
                particles.remove(p)

            # draw particle
            extra_particles = p.draw(screen)

            # add extra particles if spawned
            if not extra_particles is None:
                particles += extra_particles
            
        # spawn new firework
        if firework_count < MAX_FIREWORKS:
            firework_count += 1
            particles.append(get_random_firework())

        # Draw the screen
        pygame.display.flip()
        screen.fill((0, 0, 0))

        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
