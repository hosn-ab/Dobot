class Position:

    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def clone(self):
        return Position(self.x, self.y, self.z, self.r)

    def sum(self, position):
        self.x += position.x
        self.y += position.y
        self.z += position.z
        self.r += position.r
        return self

    def multiply(self, x, y, z):
        self.x *= x
        self.y *= y
        self.z *= z
        return self

    def sum_x(self, x):
        self.x += x
        return self

    def sum_y(self, y):
        self.y += y
        return self

    def sum_z(self, z):
        self.z += z
        return self

    def sum_r(self, r):
        self.r += r
        return self

    def change_x(self, x):
        self.x = x
        return self

    def change_y(self, y):
        self.y = y
        return self

    def change_z(self, z):
        self.z = z
        return self

    def change_r(self, r):
        self.r = r
        return self

    def __str__(self):
        return str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ', ' + str(self.r)
