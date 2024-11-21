from typing import Any, Dict
from .entity import Entity

class Tree(Entity):
    def __init__(self, x: float, y: float, data: Dict[str, Any]):
        super().__init__(x, y, data)
        self.data['type'] = 'tree'
        self.data['health'] = 50
        self.data['size'] = 5
        self.rectangle = self.get_bounds()

class Rock(Entity):
    def __init__(self, x: float, y: float, data: Dict[str, Any]):
        super().__init__(x, y, data)
        self.data['type'] = 'rock'
        self.data['health'] = 100
        self.data['size'] = 2
        self.rectangle = self.get_bounds()
        
        
class Bush(Entity):
    def __init__(self, x: float, y: float, data: Dict[str, Any]):
        super().__init__(x, y, data)
        self.data['type'] = 'bush'
        self.data['health'] = 20
        self.data['size'] = 3
        self.rectangle = self.get_bounds()
        
        
class Grass(Entity):
    def __init__(self, x: float, y: float, data: Dict[str, Any]):
        super().__init__(x, y, data)
        self.data['type'] = 'grass'
        self.data['health'] = 10
        self.data['size'] = 1
        self.rectangle = self.get_bounds()
        


        
        
