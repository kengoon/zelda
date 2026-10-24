class Group(list):
    def draw(self):
        for sprite in self:
        # for sprite in sorted(self, key=lambda sprite: sprite.center_y):
            sprite.draw()
