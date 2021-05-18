import functions
import math

class texture:
    def value(self, u, v, p):
        pass

class solid_color(texture):
    def __init__(self, color):
        self.color = color
    def value(self, u, v, p):
        return self.color

class checker_texture(texture):
    def __init__(self, _even, _odd):
        self._even = _even
        self._odd = _odd
    def value(self, u, v, p):
        sines = math.sin(10 * p[0]) * math.sin(10 * p[1]) * math.sin(10 * p[2])
        if sines < 0:
            return self._odd.value(u, v, p)
        else:
            return self._even.value(u, v, p)