import pygame
from vector2 import Vector2
from random import randint

from physics import *


class Particle:
    """A particle with a position, size, color, and lifespan.
    
    Parameters
    ----------
    position : Vector2
        The position of the particle.
    size : Vector2, optional
        The size of the particle. Defaults to (1, 1).
    color : tuple[3], optional
        The color of the particle as an RGB tuple. Defaults to (255, 0, 0).
    lifespan : int|float, optional
        The lifespan of the particle in frames. Defaults to 60.
    """
    def __init__(
            self,
            position: Vector2,
            size: Vector2 = Vector2(1, 1),
            color: tuple[int, int, int] = (255,0,0),
            lifespan: int|float = 60):

        self.position = position
        self.size = size

        self.color = color
        self.lifespan = lifespan

    def draw(self, screen):
        """Draw the particle on the given screen."""
        pygame.draw.rect(screen, self.color, (tuple(self.position), tuple(self.size)))

    def update(self) -> bool:
        """Update the particle's state.
        
        Returns
        -------
        bool
            Returns True if the particle has reached the end of its lifespan.
        """
        self.lifespan -= 1
        if self.lifespan < 0:
            return True
        return False
   
class UnstableParticle(Particle):
    """A particle with a position, size, color, lifespan, and wobbling movement.
    
    Inherits from the Particle class and adds a wobbling movement to the particle's position.
    
    Parameters
    ----------
    position : Vector2
        The position of the particle.
    size : Vector2, optional
        The size of the particle. Defaults to (1, 1).
    color : tuple[int, int, int], optional
        The color of the particle as an RGB tuple. Defaults to (255, 0, 0).
    lifespan : int|float, optional
        The lifespan of the particle in frames. Defaults to 60.
    wobbling : Vector2, optional
        The range of the wobbling movement as a Vector2 object. Defaults to (1, 1).
    """
    def __init__(self,
            position: Vector2,
            size: Vector2 = Vector2(1, 1),
            color: tuple[int, int, int] = (255,0,0),
            lifespan: int|float = 60,
            wobbling: Vector2 = Vector2(1, 1)
            ):
        super().__init__(position=position, size=size, color=color, lifespan=lifespan)
        self.wobbling = wobbling

    @property
    def wobbled_position(self):
        return self.position + Vector2(randint(-self.wobbling.x, self.wobbling.x), randint(-self.wobbling.y, self.wobbling.y))

    def draw(self, screen):
        """Draw the particle on the given screen with a wobbling movement.
        
        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the particle on.
        """
        pygame.draw.rect(
            screen, 
            self.color, 
            (
                tuple(self.wobbled_position),
                tuple(self.size)
            )
        )
    
class ExplosionParticle(UnstableParticle):
    """
    A class representing a particle that is created as part of an explosion.
    
    Inherits from UnstableParticle.
    
    Attributes:
    ----------
        position (Vector2): 
            The position of the particle.
        color (tuple[3]): 
            The color of the particle as a tuple of 3 integers representing red, green, and blue values (range 0-255).
        size (Vector2): 
            The size of the particle as a Vector2 object.
        lighten_colors (tuple[3]): A tuple of 3 integers representing how much to lighten the colors of the particle by (range 0-255).
        velocity (Vector2): 
            The velocity of the particle as a Vector2 object.
        lifetime (int): 
            The lifetime of the particle in frames.
        wobbling (Vector2): 
            The amount of wobbling applied to the particle as a Vector2 object.
        smokiness (int): 
            The number of smoke particles to generate when the particle is drawn.
        explosion_level (int): 
            The level of the explosion (used for recursive explosions).
    """
    def __init__(
        self,
        position: Vector2,
        color: tuple[3],
        size: Vector2,
        lighten_colors: tuple[3] = (0, 0, 0),
        velocity: Vector2 = Vector2(0, -10),
        lifetime: int = 100,
        wobbling: Vector2 = Vector2(2, 0),
        smokiness: int = 1,
        explosion_level: int = 1):  
        """
        Initializes an ExplosionParticle object.
        
        Args:
            position (Vector2): The position of the particle.
            color (tuple[3]): The color of the particle as a tuple of 3 integers representing red, green, and blue values (range 0-255).
            size (Vector2): The size of the particle as a Vector2 object.
            lighten_colors (tuple[3]): A tuple of 3 integers representing how much to lighten the colors of the particle by (range 0-255).
            velocity (Vector2): The velocity of the particle as a Vector2 object.
            lifetime (int): The lifetime of the particle in frames.
            wobbling (Vector2): The amount of wobbling applied to the particle as a Vector2 object.
            smokiness (int): The number of smoke particles to generate when the particle is drawn.
            explosion_level (int): The level of the explosion (used for recursive explosions).
        """
        
        color = tuple(min(color[i] + lighten_colors[i], 255) for i in range(0,3))

        super().__init__(position = position, size = size, color = color, lifespan = lifetime, wobbling = wobbling)
        self.velocity = velocity
        self.explosion_level = explosion_level-1
        self.smokiness = smokiness
    
    def draw(self, screen) -> list[UnstableParticle]:
        """
        Draws the particle on the provided screen.
        
        Args:
            screen (pygame.Surface): The screen to draw the particle on.
        
        Returns:
            list[UnstableParticle]: A list of smoke particles
        """
        # position
        position = super().wobbled_position

        # draw polygon
        rect = rotate_rectangle_by_vector_angle(position, self.size, self.velocity)
        pygame.draw.polygon(screen, self.color, rect)

        # generate smoke
        LIFETIME_RANGE = 9
        return [UnstableParticle(
            position = Vector2((rect[2][0]+ rect[3][0])/2 ,(rect[2][1]+ rect[3][1])/2),
            size = Vector2(2,2),
            color = (255,255,255),
            lifespan = randint(LIFETIME_RANGE//3, LIFETIME_RANGE)) 
        for _ in range(self.smokiness)]

    def update(self) -> bool:
        """
        Updates the particle's position and checks if it is still alive.
        
        Returns:
            bool: True if the particle is still alive, False otherwise.
        """
        G = .4
        # apply velocity
        self.position += self.velocity
        # apply gravity
        self.velocity += Vector2(0, G)

        return super().update()

    
class Firework(UnstableParticle):
    """A particle that simulates a firework explosion.
    
    Inherits from the UnstableParticle class and adds movement and smoke particles to the firework.
    
    Parameters
    ----------
    position : Vector2
        The position of the firework.
    color : tuple[3]
        The color of the firework as an RGB tuple.
    size : Vector2
        The size of the firework.
    velocity : Vector2, optional
        The velocity of the firework as a Vector2 object. Defaults to (0, -10).
    lifetime : int, optional
        The lifetime of the firework in frames. Defaults to 100.
    smokiness : int, optional
        The number of smoke particles to generate when the firework explodes. Defaults to 1.
    wobbling : Vector2, optional
        The range of the wobbling movement as a Vector2 object. Defaults to (2, 0).
    """
    def __init__(
        self,
        position: Vector2,
        color: tuple[3],
        size: Vector2,
        velocity: Vector2 = Vector2(0, -10),
        lifetime: int = 100,
        smokiness: int = 1,
        wobbling: Vector2 = Vector2(2, 0),
    ):
        super().__init__(position = position, size = size, color = color, lifespan = lifetime, wobbling = wobbling)
        # Initialize the firework's position and appearance
        self.velocity = velocity

        self.smokiness = smokiness

    def draw(self, screen) ->list[UnstableParticle]:
        """Draw the firework on the given screen and generate smoke particles.
        
        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the firework and smoke particles on.
        
        Returns
        -------
        list[UnstableParticle]
            A list of smoke particles.
        """
        super().draw(screen)

        SPREAD = 2
        LIFETIME_RANGE = 40

        return [UnstableParticle(
            position = self.position + Vector2(randint(-SPREAD, self.size.x + SPREAD), self.size.y + randint(0, SPREAD)),
            size = Vector2(2,2),
            color = (255,255,255),
            lifespan = randint(LIFETIME_RANGE//3, LIFETIME_RANGE)) 
        for _ in range(self.smokiness)]

    def update(self) -> bool:
        """Update the firework's position and check if it has reached the end of its lifespan.
        
        Returns
        -------
        bool
            Returns True if the firework has reached the end of its lifespan.
        """
        self.position += self.velocity
        return super().update()
