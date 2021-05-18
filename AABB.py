import numpy as np
import functions

class aabb:
    def __init__(self, a, b):
        self.min = a
        self.max = b
    def hit(self, r, t_min, t_max, rec):
        for i in range(3):
            t0 = min((self.min[i] - r.origin[i]) / r.direction[i], (self.max[i] - r.origin[i]) / r.direction[i])
            t1 = max((self.min[i] - r.origin[i]) / r.direction[i], (self.max[i] - r.origin[i]) / r.direction[i])
            t_min = min(t0, t_min)
            t_max = max(t1, t_max)

            if t_max <= t_min:
                return False, rec
            else:
                return True, rec
    def __str__(self):
        return "Hitbox: " + t_min.__str__() + ", " + t_max.__str__()
            