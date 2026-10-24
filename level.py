from kivent_core.managers.resource_managers import texture_manager
from kivy.utils import QueryDict

from kiventx.group import Group
from kiventx.tile import Tile
from kiventx.util import load_model
from player import Player
from settings import TILE_SIZE, WORLD_MAP


class Level:
    __slots__ = (
        "game",
        "gameworld",
        "graphics",
        "obstacle_sprites",
        "player",
        "visible_sprites",
    )

    def __init__(self, game):
        self.game = game
        self.gameworld = self.game.gameworld
        self.visible_sprites = Group()
        self.obstacle_sprites = Group()
        self.player = None
        self.graphics = QueryDict()
        self.load_texture()
        self.load_model()
        self.create_map()

    def load_texture(self):
        texture_manager.load_image("assets/test/rock.png")
        texture_manager.load_image("assets/test/player.png")

    def load_model(self):
        width, height = TILE_SIZE
        load_model(
            gameworld=self.gameworld, width=width, height=height, texture_key="rock"
        )
        load_model(
            gameworld=self.gameworld, width=width, height=height, texture_key="player"
        )

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = (col_index * TILE_SIZE[0]) + (TILE_SIZE[0] / 2)
                y = (
                    self.game.top
                    - TILE_SIZE[1]
                    - (row_index * TILE_SIZE[1])
                    + (TILE_SIZE[1] / 2)
                )

                if col == "x":
                    Tile(
                        self.gameworld,
                        "renderer_low",
                        "rock",
                        "rock",
                        TILE_SIZE,
                        (x, y),
                        [self.visible_sprites, self.obstacle_sprites],
                    )
                if col == "p":
                    self.player = Player(
                        self.obstacle_sprites,
                        self.gameworld,
                        "renderer_mid",
                        "player",
                        "player",
                        TILE_SIZE,
                        (x, y),
                        [self.visible_sprites],
                    )

    def draw(self):
        self.visible_sprites.draw()

    def update(self, dt):
        self.player.update(dt)
