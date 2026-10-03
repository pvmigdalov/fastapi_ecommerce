def non_instantiable(cls: type):
    def _new(cls, *args, **kwargs):
        raise TypeError(
            f"The class {cls.__name__} is not intended for creating instances"
        )

    cls.__new__ = _new
    return cls


class classproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(owner)
