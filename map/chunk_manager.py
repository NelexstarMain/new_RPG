"""
ChunkManager - Memory-optimized chunk management system.

Module implements caching and management of map chunks in memory,
with automatic data type optimization and stored elements limit.

Example:
    >>> manager = ChunkManager(max_chunks_in_memory=100)
    >>> chunk_data = {
    ...     'height': np.array([[0.5, 0.7], [0.3, 0.9]]),
    ...     'water': np.array([[True, False], [False, True]]),
    ...     'biome': np.array([[1, 2], [2, 3]])
    ... }
    >>> manager.add_chunk(0, 0, chunk_data)
    >>> retrieved_chunk = manager.get_chunk(0, 0)

Attributes:
    max_chunks (int): Maximum number of chunks stored in memory
    chunks (OrderedDict): Dictionary storing chunks, preserving insertion order

Main features:
    - Automatic chunk data type optimization
    - LRU caching mechanism
    - Memory usage monitoring
    - Automatic removal of oldest chunks when limit is exceeded

Chunk data types:
    - height: Height map (float32 -> uint8)
    - water: Water map (bool -> uint8)
    - biome: Biome map (uint8)

Notes:
    The class implements memory optimization by converting floating point 
    height values and boolean water values to uint8, significantly reducing 
    memory footprint while maintaining data integrity.
"""

import numpy as np
from typing import Tuple, Optional
from collections import OrderedDict

class ChunkManager:
    def __init__(self, max_chunks_in_memory: int = 100):
        """
        Zarządca chunków z cache'owaniem w pamięci.
        
        Args:
            max_chunks_in_memory: Maksymalna liczba chunków trzymanych w pamięci
        """
        self.max_chunks = max_chunks_in_memory
        self.chunks: OrderedDict[Tuple[int, int], dict] = OrderedDict()
        
    def add_chunk(self, x: int, y: int, chunk_data: dict) -> None:
        """Dodaje chunk do pamięci w zoptymalizowanej formie"""
        # Konwersja do mniejszych typów danych
        optimized_chunk = {
            'height': (chunk_data['height'] * 255).astype(np.uint8),
            'water': chunk_data['water'].astype(np.uint8),
            'biome': chunk_data['biome'].astype(np.uint8)
        }
        
        # Usuwanie najstarszego chunka jeśli przekroczono limit
        if len(self.chunks) >= self.max_chunks:
            self.chunks.popitem(last=False)
            
        self.chunks[(x, y)] = optimized_chunk
        
    def get_chunk(self, x: int, y: int) -> Optional[dict]:
        """Pobiera chunk i konwertuje go z powrotem do oryginalnego formatu"""
        chunk = self.chunks.get((x, y))
        if chunk is None:
            return None
            
        # Przeniesienie chunka na koniec kolejki (oznaczenie jako ostatnio używany)
        self.chunks.move_to_end((x, y))
        
        # Konwersja z powrotem do oryginalnych typów
        return {
            'height': chunk['height'].astype(np.float32) / 255.0,
            'water': chunk['water'].astype(bool),
            'biome': chunk['biome']
        }
    
    def get_chunk_raw(self, x: int, y: int) -> Optional[dict]:
        """Pobiera chunk w zoptymalizowanej formie bez konwersji"""
        return self.chunks.get((x, y))
    
    def remove_chunk(self, x: int, y: int) -> None:
        """Usuwa chunk z pamięci"""
        if (x, y) in self.chunks:
            del self.chunks[(x, y)]
            
    def clear(self) -> None:
        """Czyści wszystkie chunki z pamięci"""
        self.chunks.clear()
        
    @property
    def memory_usage(self) -> int:
        """Zwraca przybliżone zużycie pamięci w bajtach"""
        total_bytes = 0
        for chunk in self.chunks.values():
            total_bytes += (
                chunk['height'].nbytes +
                chunk['water'].nbytes +
                chunk['biome'].nbytes
            )
        return total_bytes

