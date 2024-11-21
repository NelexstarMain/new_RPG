from dataclasses import dataclass
from typing import Dict, Any
import uuid


@dataclass
class Rectangle:
    """
    A class representing a rectangular area in 2D space with unique identifier.

    Attributes:
        id (UUID): Unique identifier generated automatically.
        min_x (float): Minimum x-coordinate of the rectangle.
        min_y (float): Minimum y-coordinate of the rectangle.
        max_x (float): Maximum x-coordinate of the rectangle.
        max_y (float): Maximum y-coordinate of the rectangle.
    """
    id: uuid.UUID
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float):
        self.id = uuid.uuid4()  # Automatyczne generowanie UUID
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def contains_point(self, x: float, y: float) -> bool:
        """
        Check if a point is inside the rectangle.

        Args:
            x (float): X-coordinate of the point.
            y (float): Y-coordinate of the point.

        Returns:
            bool: True if point is inside rectangle, False otherwise.
        """
        return (self.min_x <= x <= self.max_x and 
                self.min_y <= y <= self.max_y)

    def intersects(self, other: 'Rectangle') -> bool:
        """
        Check if this rectangle intersects with another rectangle.

        Args:
            other (Rectangle): Another rectangle to check intersection with.

        Returns:
            bool: True if rectangles intersect, False otherwise.
        """

        return not (self.max_x < other.min_x or 
                   self.min_x > other.max_x or 
                   self.max_y < other.min_y or 
                   self.min_y > other.max_y)
    
    
@dataclass
class Entity:
    """
    A class representing a movable entity with position and custom data.

    Attributes:
        id (UUID): Unique identifier generated automatically.
        x (float): X-coordinate of the entity.
        y (float): Y-coordinate of the entity.
        data (Dict[str, Any]): Dictionary containing entity's custom data.
    """
    id: uuid.UUID
    x: float
    y: float
    data: Dict[str, Any]
    
    def __init__(self, x: float, y: float, data: Dict[str, Any]):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.data = data or {}

    def move(self, new_x: float, new_y: float) -> None:
        """
        Move entity to a new position.

        Args:
            new_x (float): New x-coordinate.
            new_y (float): New y-coordinate.
        """
        self.x = new_x
        self.y = new_y

    def update_data(self, key: str, value: Any) -> None:
        """
        Update entity's custom data.

        Args:
            key (str): Key to update or add.
            value (Any): Value to associate with the key.
        """

        self.data[key] = value

    def get_position(self) -> tuple[float, float]:
        """
        Get current position of the entity.

        Returns:
            tuple[float, float]: Current (x, y) coordinates.
        """
        return (self.x, self.y)

    def get_bounds(self) -> Rectangle:
        """
        Get rectangular bounds of the entity.

        Returns:
            Rectangle: A Rectangle instance representing entity's bounds,
                      with size determined by the 'size' value in entity's data
                      (defaults to 1.0 if not specified).
        """
        size = self.data.get('size', 1.0)
        return Rectangle(
            min_x=self.x - size,
            min_y=self.y - size,
            max_x=self.x + size,
            max_y=self.y + size
        )
        
    
