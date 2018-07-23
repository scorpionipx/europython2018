from math import pi

def dataclass(cls):
    def __init__(self, *args, **kwargs):
        for k, v in zip(cls.__annotations__.keys(), args):
            setattr(self, k, v)
        for k, v in kwargs.items():
            if k not in cls.__annotations__:
                raise TypeError(
                    f"__init__() got an unexpected keyword argument '{k}'"
                )
            setattr(self, k, v)

        post_init = getattr(self, '__post_init__', None)
        if callable(post_init):
            post_init()

    def __repr__(self):
        kwargs = {k: getattr(self, k) for k in cls.__annotations__}
        kwstr = ', '.join([f'{k}={v}' for k, v in kwargs.items()])
        return f'{cls.__name__}({kwstr})'

    setattr(cls, '__init__', __init__)
    setattr(cls, '__repr__', __repr__)
    setattr(cls, '__str__', __repr__)
    return cls


class TypeChecker:
    required_type = object

    def __init__(self, name=None):
        self.name = f'_{name}'

    def __get__(self, instance, owner=None):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        assert isinstance(value, self.required_type), \
               f'Booooo! Expecting a {self.required_type.__name__}'
        instance.__dict__[self.name] = value


def type_check(cls):
    for var_name, var_type in cls.__annotations__.items():
        class Checker(TypeChecker):
            required_type = var_type

        setattr(cls, var_name, Checker(var_name))
    return cls


class TypeCheckMeta(type):
    def __new__(meta, name, bases, dct):
        cls = super().__new__(meta, name, bases, dct)
        return type_check(cls)


class Base(metaclass=TypeCheckMeta):
    __annotations__ = {}

@dataclass
class Point(Base):
    x: int
    y: int

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy

@dataclass
class Circle(Base):
    center: Point
    radius: int

    @property
    def area(self):
        return pi * self.radius ** 2

