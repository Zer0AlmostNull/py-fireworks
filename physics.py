import math
from vector2 import *

def rotate_rectangle_by_vector_angle(center: Vector2, size: Vector2, vector: Vector2):
    """
    Rotates a rectangle around its center by the angle of a provided vector.
    
    Args:
    -------
        center (Vector2): 
            The center position of the rectangle as a Vector2 object.
        size (Vector2): 
            The size of the rectangle as a Vector2 object.
        vector (Vector2): 
            The vector to rotate the rectangle by, as a Vector2 object.
    
    Returns:
    -----------
        list[tuple[2]]: 
            A list of 4 tuples representing the rotated points of the rectangle, in the order top-left, top-right, bottom-right, bottom-left.
    """
    # Calculate the angle of the vector in radians
    angle = vector.angle
    
    # Calculate the points of the rectangle centered at the origin
    points = [
        (-size.x / 2, -size.y / 2),  # top-left
        (size.x / 2, -size.y / 2),  # top-right
        (size.x / 2, size.y / 2),  # bottom-right
        (-size.x / 2, size.y / 2)  # bottom-left
    ]
    
    # Rotate the points around the origin
    rotated_points = [(x * math.cos(angle) - y * math.sin(angle), y * math.cos(angle) + x * math.sin(angle)) for x, y in points]
    
    # Translate the points back to the center of the rectangle
    return [(x + center.x, y + center.y) for x, y in rotated_points]