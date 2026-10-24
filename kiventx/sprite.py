from kivy.vector import Vector


class Collision:
    def collision_direction(self, rect, ret_overlap=False):
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = rect.x, rect.y, rect.width, rect.height

        # Centers
        center1_x = x1 + w1 / 2
        center1_y = y1 + h1 / 2
        center2_x = x2 + w2 / 2
        center2_y = y2 + h2 / 2

        # Distances
        dx = center2_x - center1_x
        dy = center2_y - center1_y

        # Combined half-widths/heights
        combined_half_widths = (w1 + w2) / 2
        combined_half_heights = (h1 + h2) / 2

        # Check collision
        if abs(dx) < combined_half_widths and abs(dy) < combined_half_heights:
            overlap_x = combined_half_widths - abs(dx)
            overlap_y = combined_half_heights - abs(dy)

            if overlap_x < overlap_y:
                if not ret_overlap:
                    return "left" if dx < 0 else "right"
                return ("left", overlap_x) if dx < 0 else ("right", overlap_y)
            else:
                if not ret_overlap:
                    return "top" if dy > 0 else "bottom"
                return ("top", overlap_x) if dy > 0 else ("bottom", overlap_y)
        return None

    def moving_collision_direction(self, sprite, ret_overlap=False):
        """
        r = (x, y, width, height)
        v = (vx, vy) - velocity vector
        Returns: "left", "right", "top", "bottom" or None
        """
        x1, y1, w1, h1 = self.x, self.y, self.width, self.height
        x2, y2, w2, h2 = sprite.x, sprite.y, sprite.width, sprite.height
        vx1, vy1 = self.velocity
        vx2, vy2 = sprite.velocity

        # Relative velocity (object1 relative to object2)
        rel_vx = vx1 - vx2
        rel_vy = vy1 - vy2

        # Centers
        center1_x = x1 + w1 / 2
        center1_y = y1 + h1 / 2
        center2_x = x2 + w2 / 2
        center2_y = y2 + h2 / 2

        dx = center2_x - center1_x
        dy = center2_y - center1_y

        combined_half_widths = (w1 + w2) / 2
        combined_half_heights = (h1 + h2) / 2

        # Check overlap
        if abs(dx) < combined_half_widths and abs(dy) < combined_half_heights:
            overlap_x = combined_half_widths - abs(dx)
            overlap_y = combined_half_heights - abs(dy)

            # Decide based on smaller overlap
            if overlap_x < overlap_y:
                if not ret_overlap:
                    return "left" if rel_vx > 0 else "right"
                return ("left", overlap_x) if rel_vx > 0 else ("right", overlap_y)
            else:
                if not ret_overlap:
                    return "top" if rel_vy > 0 else "bottom"
                return ("top", overlap_x) if rel_vy > 0 else ("bottom", overlap_y)

        return None


class Rect(Collision):
    __slots__ = ('_pos', '_size')

    def __init__(self, pos, size):
        super().__init__()
        self._pos = Vector(pos)
        self._size = list(size)

    @property
    def pos(self):
        return self._pos[:]

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def x(self):
        return self._pos.x

    @x.setter
    def x(self, value):
        self._pos.x = value

    @property
    def y(self):
        return self._pos.y

    @y.setter
    def y(self, value):
        self._pos.y = value

    @property
    def center_x(self):
        return self.x + self.width / 2

    @center_x.setter
    def center_x(self, value):
        self.x = value - self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @center_y.setter
    def center_y(self, value):
        self.y = value - self.height / 2

    @property
    def center(self):
        return self.center_x, self.center_y

    @center.setter
    def center(self, value):
        self.center_x, self.center_y = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self.size = value

    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, value):
        self.size[0] = value

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, value):
        self.size[1] = value

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.x = value - self.width

    @property
    def top(self):
        return self.y + self.height

    @top.setter
    def top(self, value):
        self.y = value - self.height

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.y = value


class Sprite(Rect):
    __slots__ = ('direction', 'entity', 'gameworld', 'model_name', 'renderer', 'speed', 'texture_name', 'velocity')

    def __init__(self, gameworld, renderer, texture_name, model_name, size, pos, groups):
        super().__init__(pos, size)
        self.renderer = renderer
        self.gameworld = gameworld
        self.texture_name = texture_name
        self.model_name = model_name
        self.velocity = Vector(0, 0)
        self.direction = Vector(0, 0)
        self.speed = 0
        self._size = size
        self._pos = Vector(pos)
        self.entity = None
        self.groups = groups
        for group in groups:
            group.append(self)

    def _set_entity_pos(self, value):
        entity = self.gameworld.entities[self.entity]
        entity.position.pos = value

    def _set_entity_x(self, value):
        entity = self.gameworld.entities[self.entity]
        entity.position.x = value

    def _set_entity_y(self, value):
        entity = self.gameworld.entities[self.entity]
        entity.position.y = value

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._set_entity_pos(tuple(value))

    @property
    def x(self):
        return self._pos.x

    @x.setter
    def x(self, value):
        self._pos.x = value
        self._set_entity_x(value)

    @property
    def y(self):
        return self._pos.y

    @y.setter
    def y(self, value):
        self._pos.y = value
        self._set_entity_y(value)

    def inflate(self, x, y):
        rect = Rect(self.pos, self.size)
        rect.width += x
        rect.height += y
        rect.x -= x / 2
        rect.y -= y / 2
        return rect

    def move(self, dt):
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()
        self.velocity = self.direction * self.speed
        if not (self.velocity.x or self.velocity.y):
            return
        self.x += self.velocity.x
        self.y += self.velocity.y

    def collide_sprite(self, sprite):
        if self.right < sprite.x:
            return False
        if self.x > sprite.right:
            return False
        if self.top < sprite.y:
            return False
        return not self.y > sprite.top

    def draw(self):
        create_dict = {
            'position': self.pos,
            self.renderer: {
                'texture': self.texture_name,
                'model_key': self.model_name,
            }
        }
        self.entity = self.gameworld.init_entity(
            create_dict,
            ['position', self.renderer],
        )
        self.on_draw()

    def on_draw(self):
        pass
