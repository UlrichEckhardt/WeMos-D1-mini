from rgb_triplet import rgb
import math
tau = math.pi * 2

class Animation:
    def __init__(self, led_count):
        self._time = 0
        self._led_count = led_count

    def generate(self, delta):
        self._time += delta

        # startup ramp
        scale = min(1, self._time / 8) ** 1.5

        # white color base
        white_base = 0.7

        res = []
        for i in range(self._led_count):
            # angle of the current LED
            phi = i * tau / self._led_count

            color = (rgb.RED * math.sin(self._time * 1.05 + phi)
                     + rgb.GREEN * math.sin(self._time + phi)
                     + rgb.BLUE * math.sin(self._time * 0.95 + phi))
            res.append(scale * color * (1 - white_base)
                       + rgb.WHITE * white_base)
        return res

