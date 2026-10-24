from kiventx.input import KeyboardInput
from kiventx.sprite import Sprite


class Player(Sprite, KeyboardInput):
    __slots__ = ("camera", "hitbox", "obstacle_sprites", "speed")

    def __init__(self, obstacle_sprites, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obstacle_sprites = obstacle_sprites
        self.speed = 300
        self.hitbox = self.inflate(0, 0)
        self.camera = self.gameworld.system_manager["camera"]

    def on_draw(self):
        self.camera.entity_to_focus = self.entity

    def collision(self):
        for sprite in self.obstacle_sprites:
            if col_direction := self.hitbox.collision_direction(sprite.hitbox):
                if self.direction.x > 0 and col_direction == "right":  # moving right
                    self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0 and col_direction == "left":  # moving left
                    self.hitbox.left = sprite.hitbox.right
                if self.direction.y > 0 and col_direction == "top":  # moving up
                    self.hitbox.top = sprite.hitbox.bottom
                if self.direction.y < 0 and col_direction == "bottom":  # moving down
                    self.hitbox.bottom = sprite.hitbox.top

    def move(self, dt):
        if self.direction.length2() > 0:
            self.direction = self.direction.normalize()
        self.velocity = self.direction * self.speed * dt
        if not (self.velocity.x or self.velocity.y):
            return
        self.hitbox.x += self.velocity.x
        self.hitbox.y += self.velocity.y
        self.center = self.hitbox.center

    def update(self, dt):
        self.move(dt)
        self.collision()
