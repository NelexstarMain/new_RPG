"""
A class for generating height maps from input arrays by normalizing and scaling values.

The class provides functionality to convert any numerical array into a height map
within specified minimum and maximum bounds.

Example:
    >>> generator = HeightMapGenerator()
    >>> input_map = np.array([[1, 2], [3, 4]])
    >>> height_map = generator.get_height(input_map, min=0, max=100)
"""
import numpy as np
from typing import Optional
class HeightMapGenerator:
    @staticmethod
    def get_height(map: np.ndarray, min = 0, max = 256) -> Optional[np.ndarray]:
        """
        Converts input array to a height map by normalizing values to specified range.

        Args:
            map (np.ndarray): Input array to be converted to height map
            min (int, optional): Minimum value for output height map. Defaults to 0
            max (int, optional): Maximum value for output height map. Defaults to 256

        Returns:
            Optional[np.ndarray]: Normalized and scaled height map as integer array,
                                with values between min and max

        Example:
            >>> input_map = np.array([[0, 5], [10, 15]])
            >>> height_map = HeightMapGenerator.get_height(input_map, 0, 100)
            >>> print(height_map)
            [[  0  33]
             [ 67 100]]
        """
        normalized_map = (map - map.min()) / (map.max() - map.min())
        
        height_map = np.round(normalized_map * (max - min) + min).astype(np.int32)
        
        return height_map
        
        
    
