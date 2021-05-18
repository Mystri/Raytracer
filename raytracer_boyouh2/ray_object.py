class ray:
#     point3 origin
#     vec3 direction
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    def at(self,t):
        return self.origin + t * self.direction