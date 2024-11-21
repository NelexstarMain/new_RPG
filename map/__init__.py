"""
Terrain Generation Package
=========================

A comprehensive package for procedural terrain generation with chunk-based world management.

Main Components
--------------
ChunkManager
    Memory-optimized system for managing world chunks with automatic caching
    and data type optimization. Handles chunk storage, retrieval, and memory management.

HeightMapGenerator
    Utility for converting and normalizing height maps between different value ranges
    with support for various data types and optimizations.

NoiseGenerators (PerlinNoise, ValueNoise)
    Implementation of noise algorithms for terrain generation:
    - 3D Perlin Noise for coherent terrain generation
    - 2D Value Noise for additional terrain features

WorldGenerator
    Main terrain generation system combining noise algorithms to create
    realistic landscapes with biomes, water, and height variations.

Example Usage
------------
>>> from map_terrain import WorldGenerator, ChunkManager
>>> 
>>> # Initialize generators
>>> world_gen = WorldGenerator(chunk_size=512, seed=42)
>>> chunk_manager = ChunkManager(max_chunks_in_memory=100)
>>> 
>>> # Generate and store chunk
>>> chunk_data = world_gen.generate_chunk(0, 0)
>>> chunk_manager.add_chunk(0, 0, chunk_data)
>>> 
>>> # Retrieve chunk data
>>> chunk = chunk_manager.get_chunk(0, 0)
>>> height_map = chunk['height']    
>>> water_mask = chunk['water']
>>> biome_map = chunk['biome']

Package Structure
---------------
terrain_gen/
    __init__.py
    chunk_manager.py    - Chunk management and caching
    height_map.py       - Height map processing utilities
    noise.py           - Noise generation algorithms
    world_gen.py       - Main terrain generation system

Version: 1.0.0
Author: NeleXstarMain
License: MIT
"""

from .chunk_manager import ChunkManager
from .height_map import HeightMapGenerator
from .noise import PerlinNoise, ValueNoise
from .world_gen import WorldGenerator

__all__ = [
    'ChunkManager',
    'HeightMapGenerator',
    'PerlinNoise',
    'ValueNoise',
    'WorldGenerator'
]

__version__ = '1.0.0'