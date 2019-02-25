# -*- coding: utf-8 -*-
from rgb_triplet import rgb
from animations import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget
import math
tau = math.pi * 2


class LightingWidget(Widget):
    """simple widget to illustrate the lighting pattern

    This is used to develop the pattern that is displayed on an LED ring without
    requiring access to actual hardware. The pattern is supplied with a plugin.
    It also defines the number of LEDs that should be visualized.

    """

    def __init__(self, animation, **kwargs):
        super().__init__(**kwargs)

        self._animation = animation

    def prepare(self):
        self._leds = []

        with self.canvas:
            pattern = self._animation(0)
            for i, c in enumerate(pattern):
                # append the colors to our list of colors so we can adjust them lateron
                self._leds.append(Color(*c))
                x = 200 + 100 * math.cos(i * tau / len(pattern))
                y = 200 + 100 * math.sin(i * tau / len(pattern))
                Ellipse(pos=(x, y), size=(10, 10))

        # We'll update our variables in a clock
        Clock.schedule_interval(self.update_animation, 1 / 20)

    def update_animation(self, delta):
        pattern = self._animation(delta)
        for i, c in enumerate(pattern):
            self._leds[i].rgb = c


class LightingApp(App):
    def build(self):
        animation = Animation(led_count=60)
        widget = LightingWidget(animation=animation.generate)
        widget.prepare()
        return widget


if __name__ == '__main__':
    LightingApp().run()
