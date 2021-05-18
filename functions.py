import numpy as np
import math
import random

def degrees_to_radians(degrees):
    return degrees * math.pi / 180.0;
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm
def color(array):
    c = array
    c[0] = clamp(c[0], 0, 0.9999)
    c[1] = clamp(c[1], 0, 0.9999)
    c[2] = clamp(c[2], 0, 0.9999)
    c = np.multiply(255.0, c)
    return c
def sample_color(array, samples_per_pixel):

    c = np.multiply(1 / samples_per_pixel, array)
    c[0] = clamp(math.sqrt(c[0]), 0, 0.9999)
    c[1] = clamp(math.sqrt(c[1]), 0, 0.9999)
    c[2] = clamp(math.sqrt(c[2]), 0, 0.9999)
    c = np.multiply(256, c)    
    
    return c

def clamp(x, x_min, x_max):
    if x < x_min :
        return x_min
    if x > x_max :
        return x_max
    return x

def random_in_unit_sphere():
    while(True):
        p = np.random.random(3)
        p = np.multiply(2.0 ,p)
        p = np.subtract(p, np.array([1, 1, 1]))
        if (np.dot(p, p) >= 1):
            continue
        return p

def random_unit_vector():
    return normalize(random_in_unit_sphere())

def random_in_unit_disk():
    while(True):
        p = np.append(np.random.random(2), np.array([0]))
        p = np.multiply(2.0 ,p)
        p = np.subtract(p, np.array([1, 1, 0]))
        if (np.dot(p, p) >= 1):
            continue
        return p
    
