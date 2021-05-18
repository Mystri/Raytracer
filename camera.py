import numpy as np
import math
import ray_object
import functions

class camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio, aperture, focus_dist):
        self.aspect_ratio = aspect_ratio
        self.theta = functions.degrees_to_radians(vfov)
        self.h = math.tan(self.theta / 2)
        self.viewport_height = 2.0 * self.h
        self.viewport_width =  self.aspect_ratio * self.viewport_height

        self.w = functions.normalize(lookfrom - lookat)
        self.u = functions.normalize(np.cross(vup, self.w))
        self.v = np.cross(self.w, self.u)

        
        self.origin = lookfrom
        self.horizontal = np.multiply(self.viewport_width, self.u * focus_dist)
        self.vertical = np.multiply(self.viewport_height, self.v * focus_dist)
    
        self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - focus_dist * self.w

        self.lens_radius = aperture / 2
    
    def get_ray(self,s, t):
        rd = self.lens_radius * functions.random_in_unit_disk()
        offset = rd[0] * self.u + rd[1] * self.v
        return ray_object.ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)