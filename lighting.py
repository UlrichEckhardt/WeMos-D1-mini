# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget
import math
tau = math.pi * 2

WHITE = (1, 1, 1)


class LightingWidget(Widget):
    def __init__(self, **kwargs):

        if 'led_count' in kwargs:
            self._led_count = kwargs.pop('led_count')
        else:
            self._led_count = 10

        super().__init__(**kwargs)

    def prepare(self):
        self.time = 0

        with self.canvas:
            # Default ellipses
            Color(*WHITE)
            self.ellipses = [
                Ellipse(pos=(i, i), size=(10, 10)) for i in range(self._led_count)
            ]

        # We'll update our variables in a clock
        Clock.schedule_interval(self.update_animation, 1 / 20)

    def update_animation(self, delta):
        self.time += delta
        phi = self.time / 3
        count = len(self.ellipses)
        for i, e in enumerate(self.ellipses):
            dphi = i * tau / count
            e.pos = (200 + 100 * math.cos(phi + dphi), 200 + 100 * math.sin(phi + dphi))


class LightingApp(App):
    def build(self):
        widget = LightingWidget(led_count=60)
        widget.prepare()
        return widget


if __name__ == '__main__':
    LightingApp().run()
