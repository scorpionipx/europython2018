from math import pi


class TypeCheck:
    required_type = object

    def __init__(self, name=None):
        self.name = f'_{name}'

    def __get__(self, instance, owner=None):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        assert isinstance(value, self.required_type), f'Booo, expecting an {self.required_type.__name__}'
        instance.__dict__[self.name] = value

class IntType(TypeCheck):
    required_type = int


def type_check(cls):
    for variable_name, checker in cls.__dict__.items():
        if isinstance(checker, TypeCheck):
            checker.name = f'_{variable_name}'
    return cls


@type_check
class Point:
    x = IntType()
    y = IntType()

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return f'A Point at {self.x}, {self.y}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'


class PointType(TypeCheck):
    required_type = Point


class Circle:
    radius = IntType()
    center = PointType()
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def area(self):
        return pi * self.radius ** 2

    def __str__(self):
        return f'A Circle at {self.center.x}, {self.center.y} and ' + \
               f'radius {self.radius}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.center!r}, {self.radius!r})'


if __name__ == '__main__':
    pass
    p = Point(1,2)
    p.__class__.__dict__['x'].__get__(p) == p.x

