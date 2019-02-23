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
        self._time = 0
        self._leds = []

        with self.canvas:
            for i in range(self._led_count):
                # append the colors to our list of colors so we can adjust them lateron
                self._leds.append(Color(*WHITE))
                x = 100 + 100 * math.cos(i * tau / self._led_count)
                y = 100 + 100 * math.sin(i * tau / self._led_count)
                Ellipse(pos=(x, y), size=(10, 10))

        # We'll update our variables in a clock
        Clock.schedule_interval(self.update_animation, 1 / 20)

    def update_animation(self, delta):
        pattern = self._animation(delta)

        for i in range(self._led_count):
            self._leds[i].rgb = pattern[i]

    def _animation(self, delta):
        self._time += delta

        res = []
        for i in range(self._led_count):
            # angle of the current LED
            phi = i * tau / self._led_count
            r = math.sin(self._time * 1.05 + phi)
            g = math.sin(self._time + phi)
            b = math.sin(self._time * 0.95 + phi)
            res.append((r, g, b))
        return res


class LightingApp(App):
    def build(self):
        widget = LightingWidget(led_count=60)
        widget.prepare()
        return widget


if __name__ == '__main__':
    LightingApp().run()
