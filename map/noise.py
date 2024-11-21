"""
Implementation of Perlin Noise and Value Noise algorithms for procedural noise generation.

This module provides implementations of two noise generation algorithms:
- Perlin Noise: 3D coherent noise generation using Ken Perlin's improved algorithm
- Value Noise: 2D noise generation using value interpolation

Both implementations are deterministic and can be seeded for reproducible results.
"""

from typing import Dict, List, Tuple, Optional
import random
import math
from dataclasses import dataclass

@dataclass
class Vector3D:
    """Represents a 3D vector with x, y, z coordinates."""
    x: float
    y: float 
    z: float

class PerlinNoise:
    def __init__(self) -> None:
        """Initializes the Perlin Noise generator with a randomized permutation table."""
        self.permutation: List[int] = list(range(256))
        random.shuffle(self.permutation)
        self.permutation *= 2

    @staticmethod
    def fade(t: float) -> float:
        """
        Applies smoothing function for interpolation.

        Args:
            t: Input value to be smoothed

        Returns:
            Smoothed value using 6t^5 - 15t^4 + 10t^3
        """
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def lerp(t: float, a: float, b: float) -> float:
        """
        Performs linear interpolation between two values.

        Args:
            t: Interpolation factor between 0 and 1
            a: First value
            b: Second value

        Returns:
            Interpolated value
        """
        return a + t * (b - a)

    def grad(self, hash: int, x: float, y: float, z: float) -> float:
        """
        Calculates gradient value for given hash and coordinates.

        Args:
            hash: Hash value from permutation table
            x: X coordinate
            y: Y coordinate
            z: Z coordinate

        Returns:
            Gradient value
        """
        h: int = hash & 15
        u: float = x if h < 8 else y
        v: float = y if h < 4 else x if h == 12 or h == 14 else z
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

    def noise(self, x: float, y: float, z: float) -> float:
        """
        Generates 3D Perlin noise value for given coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate

        Returns:
            Noise value typically in range [-1, 1]
        """
        X: int = int(math.floor(x)) & 255
        Y: int = int(math.floor(y)) & 255
        Z: int = int(math.floor(z)) & 255

        x -= math.floor(x)
        y -= math.floor(y)
        z -= math.floor(z)

        u: float = self.fade(x)
        v: float = self.fade(y)
        w: float = self.fade(z)

        A: int = self.permutation[X] + Y
        AA: int = self.permutation[A] + Z
        AB: int = self.permutation[A + 1] + Z
        B: int = self.permutation[X + 1] + Y
        BA: int = self.permutation[B] + Z
        BB: int = self.permutation[B + 1] + Z

        return self.lerp(w,
            self.lerp(v,
                self.lerp(u,
                    self.grad(self.permutation[AA], x, y, z),
                    self.grad(self.permutation[BA], x-1, y, z)
                ),
                self.lerp(u,
                    self.grad(self.permutation[AB], x, y-1, z),
                    self.grad(self.permutation[BB], x-1, y-1, z)
                )
            ),
            self.lerp(v,
                self.lerp(u,
                    self.grad(self.permutation[AA+1], x, y, z-1),
                    self.grad(self.permutation[BA+1], x-1, y, z-1)
                ),
                self.lerp(u,
                    self.grad(self.permutation[AB+1], x, y-1, z-1),
                    self.grad(self.permutation[BB+1], x-1, y-1, z-1)
                )
            )
        )

class ValueNoise:
    def __init__(self, seed: Optional[int] = None) -> None:
        """
        Initializes Value Noise generator.

        Args:
            seed: Optional seed for random number generation
        """
        random.seed(seed)
        self.grid: Dict[Tuple[int, int], float] = {}

    def get_value(self, x: float, y: float) -> float:
        """
        Gets or generates a value for given coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Random value for given coordinates
        """
        coords: Tuple[int, int] = (int(x), int(y))
        if coords not in self.grid:
            self.grid[coords] = random.random()
        return self.grid[coords]

    def smooth_noise(self, x: float, y: float) -> float:
        """
        Generates smoothed noise value for given coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Smoothed noise value
        """
        corners: float = (self.get_value(math.floor(x), math.floor(y)) +
                        self.get_value(math.floor(x), math.ceil(y)) +
                        self.get_value(math.ceil(x), math.floor(y)) +
                        self.get_value(math.ceil(x), math.ceil(y))) / 16
        sides: float = (self.get_value(math.floor(x), y) +
                       self.get_value(x, math.floor(y)) +
                       self.get_value(math.ceil(x), y) +
                       self.get_value(x, math.ceil(y))) / 8
        center: float = self.get_value(x, y) / 4
        return corners + sides + center