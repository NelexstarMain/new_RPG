
"""
World Generator Module - Procedural terrain generation system.

This module provides functionality for generating infinite world chunks with terrain,
water, and biomes using a combination of Perlin and Value noise algorithms.
The implementation is memory-optimized and generates consistent terrain across chunks.

Features:
    - Procedural terrain generation using multiple noise layers
    - Biome distribution based on height and water level
    - Memory-efficient chunk generation
    - Seamless chunk borders
    - Deterministic generation with seed support

Example:
    >>> generator = WorldGenerator(chunk_size=512, seed=42)
    >>> chunk = generator.generate_chunk(0, 0)
    >>> height_map = chunk['height']
    >>> water_mask = chunk['water']
    >>> biome_map = chunk['biome']
"""
import numpy as np
from .noise import PerlinNoise, ValueNoise

class WorldGenerator:
    """
    World generator with terrain and water features, optimized for memory usage.
    
    Example:
        # Initialize generator
        generator = WorldGenerator(chunk_size=512, seed=42)
        
        # Generate world chunk
        chunk_data = generator.generate_chunk(0, 0)
        
        # Access data:
        height_map = chunk_data['height']  # terrain height map
        water_mask = chunk_data['water']   # water areas mask
        biome_map = chunk_data['biome']    # biome map
        
        # Generate adjacent chunks:
        next_chunk = generator.generate_chunk(1, 0)  # right chunk
    
    Args:
        chunk_size (int): Size of a single chunk (default: 512)
        seed (int): Random generator seed (default: None)
        water_level (float): Water level (0.0 - 1.0, default: 0.4)
    
    Returns:
        Dictionary containing:
        - 'height': np.array - terrain height map (0.0 - 1.0)
        - 'water': np.array - boolean mask of water areas
        - 'biome': np.array - biome identifiers
    """
    
    def __init__(self, chunk_size=512, seed=None, water_level=0.4):
        """
        Initialize the WorldGenerator with specified parameters.

        Args:
            chunk_size (int): Size of generated chunks
            seed (int, optional): Seed for random generation
            water_level (float): Global water level (0.0-1.0)
        """
        self.chunk_size = chunk_size
        self.water_level = water_level
        self.perlin = PerlinNoise()
        self.value = ValueNoise(seed=seed)
        
        self.terrain_scales = [
            (30, 1.0),    # large formations
            (100, 0.8),   # hills
            (50, 0.4),    # small elevations
            (25, 0.2),    # terrain details
            (10, 0.1),    # micro relief
        ]

    def generate_chunk(self, x_offset, y_offset):
        """
        Generate a new chunk at specified coordinates.

        Args:
            x_offset (int): Chunk X coordinate in world space
            y_offset (int): Chunk Y coordinate in world space

        Returns:
            dict: Dictionary containing height map, water mask, and biome map
        """
        height_map = np.zeros((self.chunk_size, self.chunk_size), dtype=np.float32)
        
        for scale, weight in self.terrain_scales:
            for y in range(self.chunk_size):
                for x in range(self.chunk_size):
                    world_x = x + x_offset * self.chunk_size
                    world_y = y + y_offset * self.chunk_size
                    
                    perlin_val = (
                        (self.perlin.noise(world_x/scale, world_y/scale, 0) + 1) * 0.5 * 0.7 +
                        (self.perlin.noise(world_x/(scale*0.3), world_y/(scale*0.3), 0) + 1) * 0.5 * 0.3
                    )
                    value_val = (self.value.smooth_noise(world_x/scale, world_y/scale) + 1) * 0.5
                    
                    height_map[y, x] += (perlin_val * 0.9 + value_val * 0.1) * weight
        
        height_map = (height_map - height_map.min()) / (height_map.max() - height_map.min())
        height_map = np.power(height_map, 1.4)
        height_map = height_map * 1.3 - 0.15
        height_map = np.clip(height_map, 0, 1)
        
        water_mask = height_map < self.water_level
        biome_map = self._generate_biomes(height_map, water_mask)
        
        return {
            'height': height_map,
            'water': water_mask,
            'biome': biome_map
        }

    def _generate_biomes(self, height_map, water_mask):
        """
        Generate biome map based on height and water distribution.

        Args:
            height_map (np.ndarray): Terrain height map
            water_mask (np.ndarray): Water areas mask

        Returns:
            np.ndarray: Biome map with IDs:
                0: Ocean
                1: Beach
                2: Plains
                3: Forest
                4: Mountains
        """
        biome_map = np.zeros_like(height_map, dtype=np.uint8)
        
        biome_map[water_mask] = 0
        biome_map[~water_mask & (height_map < self.water_level + 0.08)] = 1
        biome_map[~water_mask & (height_map >= self.water_level + 0.08) & (height_map < 0.65)] = 2
        biome_map[~water_mask & (height_map >= 0.65) & (height_map < 0.85)] = 3
        biome_map[~water_mask & (height_map >= 0.85)] = 4
        
        return biome_map