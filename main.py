from kivy.app import App
from kivy.clock import Clock, triggered
from kivy.config import Config
from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.widget import Widget

Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "720")

from kivent_core.systems.gamesystem import GameSystem


class MyAnimationSystem(GameSystem):
    _update_to_make = ListProperty()

    def register_update_to_make(self, method):
        self._update_to_make.append(method)

    def update(self, dt):
        for make_update in self._update_to_make:
            make_update()


Factory.register('MyAnimationSystem', cls=MyAnimationSystem)


class Game(Widget):
    gameworld = ObjectProperty()
    camera = ObjectProperty()
    animation_system = ObjectProperty()
    level = ObjectProperty()

    def on_kv_post(self, base_widget):
        self.gameworld.init_gameworld(
            ['position', 'renderer_low', 'renderer_mid', 'renderer_high', 'camera', 'animation'],
            callback=self.init_game
        )

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.level = Level(self)
        self.level.draw()
        self.camera = self.gameworld.system_manager['camera']
        self.animation_system = self.gameworld.system_manager['animation']
        self.animation_system.register_update_to_make(self.level.update)

    def setup_states(self):
        self.gameworld.add_state(
            state_name='main',
            systems_added=['position', 'animation', 'renderer_low', 'renderer_mid', 'renderer_high', 'camera'],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=['position', 'animation', 'renderer_low', 'renderer_mid', 'renderer_high', 'camera'],
            screenmanager_screen='main'
        )

    def set_state(self):
        self.gameworld.state = 'main'


class DebugPanel(Widget):
    fps = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_fps()

    @triggered(0.05, True)
    def update_fps(self):
        self.fps = str(int(Clock.get_fps()))


class GameApp(App):
    pass


if __name__ == '__main__':
    GameApp().run()