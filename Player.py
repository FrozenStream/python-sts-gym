from Entity import Entity

class Player(Entity):
    """玩家类"""
    def __init__(self, name: str, max_hp: int):
        super().__init__(name, max_hp)

