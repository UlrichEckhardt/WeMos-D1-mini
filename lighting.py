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
        self._time += delta

        for i in range(self._led_count):
            dphi = i * tau / self._led_count
            self._leds[i].rgb = (
                (1 + math.sin(self._time + dphi)) / 2,
                (1 + math.sin(self._time + 1.1 * dphi + tau / 3)) / 2,
                (1 + math.sin(self._time + dphi ** 1.1 + 2 * tau / 3)) / 2,
            )


class LightingApp(App):
    def build(self):
        widget = LightingWidget(led_count=60)
        widget.prepare()
        return widget


if __name__ == '__main__':
    LightingApp().run()
