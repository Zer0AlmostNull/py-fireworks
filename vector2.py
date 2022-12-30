from math import sqrt, atan2

class Vector2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x, y)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2(x, y)
    
    def __tuple__(self):
        return (self.x, self.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            x = self.x * other.x
            y = self.y * other.y
            return Vector2(x, y)
        else:
            return Vector2(self.x * other, self.y * other)
    
    def __div__(self, other):
        if isinstance(other, Vector2):
            x = self.x / other.x
            y = self.y / other.y
            return Vector2(x, y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            x = self.x / other.x
            y = self.y / other.y
            return Vector2(x, y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __itruediv__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other

    def __pow__(self, other):
        x = self.x ** other
        y = self.y ** other
        return Vector2(x, y)

    def __iter__(self):
        yield self.x
        yield self.y
        
    def copy(self) -> 'Vector2':
        """
        Returns a copy of the Vector2 object.
        """
        return Vector2(self.x, self.y)
        
    def __eq__(self, other):
        return (other.x == self.x and other.y == self.y)
    
    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    @property
    def angle(self) -> float:
        """
        Returns the angle of the vector in radians.
        
        Returns:
            float: The angle of the vector in radians.
        """
        return atan2(self.y, self.x)
    
    @property
    def length(self) -> float:
        """
        Returns the length or magnitude of the vector.
        
        Returns:
        The length of the vector.
        
        Example:
        >>> v = Vector2(3, 4)
        >>> v.length
        5.0
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    @property
    def normalized(self) -> 'Vector2':
        """
        Returns a new vector that has the same direction as the original vector, but with a length of 1.
        
        Returns:
        The normalized vector.
        
        Example:
        >>> v = Vector2(3, -4)
        >>> v.normalized
        Vector2(1, -1)
        """
        norm = lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
        return Vector2(norm(self.x), norm(self.y))
    
    def to_unit_vector(self) -> 'Vector2':
        """
        Returns a new vector that has the same direction as the original vector, but with a length of 1.
        
        Returns:
        The unit vector.
        
        Example:
        >>> v = Vector2(3, 4)
        >>> v.to_unit_vector()
        Vector2(0.6, 0.8)
        """
        length = self.length
        if length != 0:
            return self.copy()/length
        else:
            return self.copy()

    @staticmethod
    def direction(o1: 'Vector2', o2: 'Vector2'):
        """
        Returns a new vector that represents the direction from o1 to o2.
        
        Parameters:
        - o1: The starting point.
        - o2: The ending point.
        
        Returns:
        The direction from o1 to o2.
        
        Example:
        >>> v1 = Vector2(0, 0)
        >>> v2 = Vector2(3, 4)
        >>> Vector2.direction(v1, v2)
        Vector2(3, 4)
        """  
        return Vector2(o1.x - o2.x, o1.y - o2.y)

    @staticmethod
    def distance(o1: 'Vector2', o2: 'Vector2') -> float:
        """
        Returns the distance between o1 and o2.
        
        Parameters:
        - o1: The first point.
        - o2: The second point.
        
        Returns:
        The distance between o1 and o2.
        
        Example:
        >>> v1 = Vector2(0, 0)
        >>> v2 = Vector2(3, 4)
        >>> Vector2.distance(v1, v2)
        5.0
        """
        return sqrt((o2.x - o1.x)**2 + (o2.y - o1.y)**2)
    
    @staticmethod
    def zero() -> 'Vector2':
        """
        Returns a new vector with both components set to 0.
        
        Returns:
        The zero vector.
        
        Example:
        >>> Vector2.zero()
        Vector2(0, 0)
        """
        return Vector2(0, 0)