# material defines reflect direction and reflected color.
import numpy as np
import math
import tex
from functions import *
from ray_object import *

class material:
    def scatter(self, r_in, rec):
        pass
    def emitted(self, u, v, p):
        return np.array([0, 0, 0])
class lambertian(material):
    def __init__(self, albedo : tex.texture):
        self.a = albedo

    def scatter(self, r_in, rec):
        scatter_direction = rec.normal + random_unit_vector()
        
        if np.isclose(scatter_direction, np.array([0, 0, 0])).all():
            scatter_direction = rec.normal
            
        scattered = ray(rec.p, scatter_direction)
        attenuation = self.a.value(rec.u, rec.v, rec.p)
        return (True, scattered, attenuation)

def reflect(v, N):
    return v - 2.0 * np.dot(v, N) * N
class metal(material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1
    def scatter(self, r_in, rec):
        reflected = reflect(normalize(r_in.direction), rec.normal)
        scattered = ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo
        return (np.dot(scattered.direction, rec.normal) > 0, scattered, attenuation)

def refract(uv, n, etai_over_etat):
    cos_theta = min(np.dot(-uv, n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta*n);
    r_out_parallel = -math.sqrt(abs(1.0 - np.dot(r_out_perp, r_out_perp))) * n;
    return r_out_perp + r_out_parallel
class dielectric(material):
    def __init__(self, index_of_refraction):
        self.index_of_refraction = index_of_refraction
    def scatter(self, r_in, rec):
        attenuation = np.array([1, 1, 1])
        refraction_ratio = (1.0 / self.index_of_refraction) if rec.front_face else self.index_of_refraction
        unit_direction = normalize(r_in.direction)
        
        cos_theta = min(np.dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
        cannot_refract = refraction_ratio * sin_theta > 1.0
        
        if (cannot_refract):
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refraction_ratio)
        
        scattered = ray(rec.p, direction)
        return True, scattered, attenuation 

class diffuse_light(material):
    def __init__(self, tex):
        self.emit = tex
    def scatter(self, r_in, rec):
        return False, r_in, self.emit.color
    def emitted(self, u, v, p):
        return self.emit.value(u, v, p) 