import numpy as np
import math
import random
from materials import *
import AABB
import ray_object
from functools import cmp_to_key
import tex

# point, normal, t, 
class hit_record:
    def __init__(self, p = np.array([0, 0, 0]), normal = np.array([0, 0, 0]), t = 0, material = lambertian(tex.solid_color(np.array([0, 0, 0])))):
        self.p = p
        self.normal = normal
        self.t = t
        self.u = 0
        self.v = 0
        self.material = material

    def set_face_normal(self, r, outward_normal):
        self.front_face = np.dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face  else -outward_normal;

        
class hittable:
    def hit(self, ray, t_min, t_max, rec):
        pass
    def bounding_box(self):
        pass

class sphere(hittable):
#     Vec3 center
#     float radius
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def get_sphere_uv(self, p, u, v):
        theta = math.acos(-p[1])
        phi = math.atan2(-p[2], p[0]) + math.pi
        u = phi / 2 * math.pi
        v = theta / math.pi
    
#     Hit function: return hit/non-hit for t in [t_min, t_max] and update hit_record if hit. 
    def hit(self, r, t_min, t_max, rec):
        AC = np.subtract(r.origin, self.center)
        a = np.dot(r.direction, r.direction)
        half_b = np.dot(r.direction, AC)
        c = np.dot(AC, AC) - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if (discriminant < 0) :
            return False, rec
        
        sqrtd = math.sqrt(discriminant)
        root = (-float(half_b) - float(sqrtd) ) / float(a)
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False, rec
        rec.t = root
        rec.p = r.at(rec.t)
        rec.material = self.material
        outward_normal = (np.subtract(rec.p, self.center)) / self.radius
        rec.set_face_normal(r, outward_normal)
        self.get_sphere_uv(outward_normal, rec.u, rec.v)
        return True, rec

    def bounding_box(self):
        output_box = AABB.aabb(self.center - np.array([self.radius, self.radius, self.radius]),
         self.center + np.array([self.radius, self.radius, self.radius]))
        return True, output_box

class xy_rect(hittable):
    def __init__(self, x0, x1, y0, y1, k, material):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.k = k
        self.material = material
    def hit(self, r, t_min, t_max, rec):
        t = (self.k - r.origin[2]) / r.direction[2]
        if t < t_min or t_max < t:
            return False, rec

        x = r.origin[0] + t * r.direction[0]
        y = r.origin[1] + t * r.direction[1]
        if x < self.x0 or self.x1 < x or y < self.y0 or self.y1 < y:
            return False, rec
        
        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (y - self.y0) / (self.y1 - self.y0)
        rec.t = t

        outward_normal = np.array([0, 0, 1])
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material
        rec.p = r.at(t);
        return True, rec

    def bounding_box(self):
        out_box = AABB.aabb(np.array([self.x0, self.y0, self.k - 0.0001]), np.array([self.x0, self.y0, self.k + 0.0001]))
        return True, out_box

class xz_rect(hittable):
    def __init__(self, x0, x1, z0, z1, k, material):
        self.x0 = x0
        self.x1 = x1
        self.z0 = z0
        self.z1 = z1
        self.k = k
        self.material = material
    def hit(self, r, t_min, t_max, rec):
        t = (self.k - r.origin[1]) / r.direction[1]
        if t < t_min or t_max < t:
            return False, rec

        x = r.origin[0] + t * r.direction[0]
        z = r.origin[2] + t * r.direction[2]
        if x < self.x0 or self.x1 < x or z < self.z0 or self.z1 < z:
            return False, rec
        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t

        outward_normal = np.array([0, 1, 0])
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material
        rec.p = r.at(t);
        return True, rec

    def bounding_box(self):
        out_box = AABB.aabb(np.array([self.x0, self.z0, self.k - 0.0001]), np.array([self.x0, self.z0, self.k + 0.0001]))
        return True, out_box

class yz_rect(hittable):
    def __init__(self, y0, y1, z0, z1, k, material):
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.k = k
        self.material = material
    def hit(self, r, t_min, t_max, rec):
        t = (self.k - r.origin[0]) / r.direction[0]
        if t < t_min or t_max < t:
            return False, rec

        y = r.origin[1] + t * r.direction[1]
        z = r.origin[2] + t * r.direction[2]
        if y < self.y0 or self.y1 < y or z < self.z0 or self.z1 < z:
            return False, rec
        rec.u = (y - self.y0) / (self.y1 - self.y0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t

        outward_normal = np.array([0, 1, 0])
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material
        rec.p = r.at(t);
        return True, rec

    def bounding_box(self):
        out_box = AABB.aabb(np.array([self.y0, self.z0, self.k - 0.0001]), np.array([self.y0, self.z0, self.k + 0.0001]))
        return True, out_box

class hittable_list(hittable):
    def __init__(self):
        self.objects = []
    def add(self, obj):
        self.objects.append(obj)
    def clear(self):
        self.objects = []
    
    
    def hit(self, r, t_min, t_max, rec):
        temp_rec = hit_record()
        hit_anything = False
        temp_closest = t_max
        record = hit_record()
        
        for obj in self.objects:
            if obj.hit(r, t_min, temp_closest, temp_rec):
                hit_anything = True
                temp_closest = temp_rec.t
                record = temp_rec

                
        return (hit_anything,record)


# ------------------------
# bvh
# ------------------------



def surrounding_box(box0, box1):
    small = np.array([min(box0.min[0], box1.min[0]), min(box0.min[1], box1.min[1]), min(box0.min[2], box1.min[2])])
    large = np.array([max(box0.max[0], box1.max[0]), max(box0.max[1], box1.max[1]), max(box0.max[2], box1.max[2])])
    return AABB.aabb(small, large)



class bvh_node(hittable):

    def __init__(self, src_objects, start, end):
        # a and b are nodes
        def box_compare(a, b, axis):
            have_box_a, box_a = a.bounding_box()
            have_box_b, box_b = b.bounding_box()
            if not have_box_a or not have_box_b:
                print ("err")
                return 0

            return box_a.min[axis] - box_b.min[axis]

        def box_x_compare(a, b):
            return box_compare(a, b, 0)
            
        def box_y_compare(a, b):
            return box_compare(a, b, 1)
            
        def box_z_compare(a, b):
            return box_compare(a, b, 2)


        # Hittable_list
        self.objects = src_objects
        axis = random.randint(0, 2)
        if axis == 0:
            comparator = box_x_compare
        if axis == 1:
            comparator = box_y_compare
        else:
            comparator = box_z_compare

        object_span = end - start


        if object_span == 1:
            self.left = self.objects.objects[start]
            self.right = self.objects.objects[start]
        elif object_span == 2:
            if comparator(self.objects.objects[start], self.objects.objects[start + 1]) < 0:
                self.left = self.objects.objects[start]
                self.right = self.objects.objects[start + 1]
            else:
                self.left = self.objects.objects[start + 1]
                self.right = self.objects.objects[start]
        else:
            self.objects.objects[start:end] = sorted(self.objects.objects[start:end], key = cmp_to_key(comparator))
            mid = int(start + object_span / 2)
            self.left = bvh_node(self.objects, start, mid)
            self.right = bvh_node(self.objects, mid, end)
        
        if not self.left.bounding_box()[0] or not self.left.bounding_box()[0]:
            print ("err")
            return
        
        box_left = self.left.bounding_box()[1]
        box_right = self.right.bounding_box()[1]

        self.box = surrounding_box(box_left, box_right)




    def hit(self, r, t_min, t_max, rec):

        # hit functions of aabbs
        test, rec = self.box.hit(r, t_min, t_max, rec)
        if not test:
            return False, rec
        hit_left, rec = self.left.hit(r, t_min, t_max, rec)
        if hit_left :
            temp = rec.t
        else:
            temp = t_max
        # print(self.right)
        hit_right, rec = self.right.hit(r, t_min, temp, rec)
        return hit_left or hit_right, rec

    def bounding_box(self):
        output_box = self.box
        return True, output_box

    def __str__(self):
        if not self.left.bounding_box()[0] or not self.left.bounding_box()[0]:
            return "end"
        return "(" + self.bounding_box().__str__() + ") \n" + self.left.__str__() + self.right.__str__()



# ---------------
# instances
# ---------------

class translate(hittable):
    def __init__(self, p, displacement):
        self.ptr = p
        self.offset = displacement

    def hit(self, r, t_min, t_max, rec):
        moved_r = ray_object.ray(r.origin - self.offset, r.direction)
        hit, rec = self.ptr.hit(moved_r, t_min, t_max, rec)
        if not hit:
            return False, rec

        rec.p += self.offset
        rec.set_face_normal(moved_r, rec.normal)
        return True, rec

    def bounding_box(self):
        if not self.ptr.bounding_box()[0]:
            return False, self.ptr.bounding_box()[1]
        else:
            output_box = self.ptr.bounding_box()[1]
            output_box = AABB.aabb(output_box.min + self.offset, output_box.max + self.offset)
            return True, output_box