from kivy.core.window import Window


class KeyboardInput:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._keyset = set()

        self._keymap = {
            ord('w'): ('y', 1),
            ord('s'): ('y', -1),
            ord('a'): ('x', -1),
            ord('d'): ('x', 1),

            273: ('y', 1),
            274: ('y', -1),
            275: ('x', 1),
            276: ('x', -1),
        }

        Window.bind(
            on_key_down=self._input,
            on_key_up=self._cancel_movement
        )

    def _input(self, window, key, scancode, text, modifiers):
        lookup = ord(text) if text else key

        if lookup in self._keymap:
            self._keyset.add(lookup)
            self._update_direction()

    def _cancel_movement(self, window, key, *_):
        self._keyset.discard(key)

        if key in self._keymap:
            self._update_direction()

    def _update_direction(self):
        x = 0
        y = 0

        for key in self._keyset:
            axis, value = self._keymap[key]

            if axis == 'x':
                x = value
            else:
                y = value

        self.direction.x = x
        self.direction.y = y