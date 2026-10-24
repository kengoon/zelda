from kiventx.sprite import Sprite


class Tile(Sprite):
    __slots__ = ('hitbox', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hitbox = self.inflate(0, 0)
