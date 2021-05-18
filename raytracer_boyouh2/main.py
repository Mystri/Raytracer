# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import math
import random

from PIL import Image

from ray_object import *
from hittable import *
from camera import *
from materials import *
from functions import *
import tex


# %%
# return the color of a ray
# form: np.array(1, 1, 1)
# world: hittable_list of all objects
def ray_color(r, background, world, depth):
    rec = hit_record()
    if (depth <= 0):
        return np.array([0, 0, 0])
    
    hit_something, rec = world.hit(r, 1, math.inf, rec)
    if (hit_something):
        has_reflection,scattered, attenuation = rec.material.scatter(r, rec)
        emitted = rec.material.emitted(rec.u, rec.v, rec.p)
        if (has_reflection):
            return (emitted + np.multiply(attenuation, ray_color(scattered, background, world, depth - 1)))
        return emitted
    
    # No Object hit (Background)
    # return np.array([0, 0, 0])
    return background


# %%
# main

# Image
print ("Input image width:")
image_width = int(input())
print ("Input image height:")
image_height = int(input())
aspect_ratio = image_width / image_height

print ("Input samples per pixel:")
samples_per_pixel = int(input())

print ("Input max depth:")
max_depth = int(input())
R = math.pi / 4
background_light = 0
background = np.array([0.70, 0.80, 1.00]) if background_light else np.array([0, 0, 0])

# PIL preprocessing to use PIL coordinates
img = Image.new(mode = "RGB", size = (image_width, image_height), color = 0)
img_array = np.array(img)
img_array = np.swapaxes(img_array, 1, 0)



# World object list
world = hittable_list()
# material config
material_solid_color = lambertian(tex.solid_color(np.array([0.59, 0.07, 0.20])))

white = tex.solid_color(np.array([0.8, 0.8, 0.8]))
black = tex.solid_color(np.array([0.2, 0.2, 0.2]))
material_checker = lambertian(tex.checker_texture(white, black))
material_dielectric = dielectric(1.5)
material_metal = metal(np.array([0.8, 0.6, 0.2]), 0.3)
material_white_light = diffuse_light(tex.solid_color(np.array([7, 7, 7])))
material_green_light = diffuse_light(tex.solid_color(np.array([2, 5, 5])))



sphere_lambertian_solid_small = sphere(np.array([0, 0.3, 0]), 0.3, material_solid_color)
sphere_lambertian_solid_checker = sphere(np.array([0, 1, 0]), 1, material_checker)


sphere_dielectric_outer = sphere(np.array([0, 0.3, 0]), 0.3, material_dielectric)
sphere_dielectric_inner = sphere(np.array([0, 0.3, 0]), -0.27, material_dielectric)

sphere_metal = sphere(np.array([0, 0.3, 0]), 0.3, material_metal)
sphere_light = sphere(np.array([0, 0.3, 0]), 0.3, material_green_light)


#adding to world

num_spheres = 7
for i in range(0, num_spheres):
    world.add(translate(sphere_metal, np.array([random.random() * 8 - 4, 0, random.random() * 8 - 4])))
    world.add(translate(sphere_lambertian_solid_small, np.array([random.random() * 8 - 4, 0, random.random() * 8 - 4])))
    world.add(translate(sphere_dielectric_outer, np.array([random.random() * 8 - 4, 0, random.random() * 8 - 4])))
    world.add(translate(sphere_dielectric_inner, np.array([random.random() * 8 - 4, 0, random.random() * 8 - 4])))
    world.add(translate(sphere_light, np.array([random.random() * 8 - 4, 0, random.random() * 6 - 3])))

world.add(translate(sphere_lambertian_solid_checker, np.array([random.random() * 6 - 3, 0, random.random() * 6 - 3])))
world.add(translate(sphere_lambertian_solid_checker, np.array([random.random() * 6 - 3, 0, random.random() * 6 - 3])))


# ground
ground = xz_rect(-20, 20, -20, 20, -0.5, material_checker)
world.add(ground)

# lighting
light_plane = yz_rect(-3, 5, -3, 5, 10, material_white_light)
light_plane_2 = yz_rect(-3, 5, -3, 5, -10, material_white_light)
light_plane_3 = xy_rect(-3, 3, -3, 5, -10, material_white_light)

world.add(light_plane)
world.add(light_plane_2)
world.add(light_plane_3)



bvh = bvh_node(world, 0, len(world.objects))


# Camera
lookfrom = np.array([4, 10, 20])
lookat = np.array([0, 0, 0])
vup = np.array([0, 1, 0])
focus_dist = 10.0
aperture = 0.1
cam = camera(lookfrom, lookat,vup, 20, aspect_ratio, aperture, focus_dist)


# Render
print("image width: ", image_width," image height: ", image_height)
for j in reversed(range(image_height)):
    if j % 10 == 0:
        print(j, "/", image_height, "Scanlines remaining")
    for i in range(image_width):
        pixel_color = np.array([0.0, 0.0, 0.0])
        for s in range(samples_per_pixel):
            u = (i + random.random()) / (image_width - 1)
            v = (j + random.random()) / (image_height - 1)
            r = cam.get_ray(u, v)
            pixel_color += ray_color(r, background, bvh, max_depth)
        img_array[i][j] = sample_color(pixel_color, samples_per_pixel)


print("Done")


# %%
final_img_array = np.swapaxes(img_array, 1, 0)
final_img_array = np.flip(final_img_array, 0)
new_pic = Image.fromarray(final_img_array.astype('uint8'), 'RGB')
new_pic.save("pictures/final_" + str(image_width) + "_" + str(image_height) + ".png", "PNG")
new_pic.show()


