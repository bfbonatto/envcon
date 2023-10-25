import inspect
import os

class _Field:
    def __init__(self, cls, field, var, fn, default):
        self.cls = cls
        self.field = field
        self.var = var
        self.fn = fn
        self.default = default

    def load(self):
        if self.var in os.environ:
            setattr(self.cls, self.field, self.fn(os.environ[self.var]))
        else:
            if self.default is not None:
                setattr(self.cls, self.field, self.default)

def _load(fields):
    def load(_):
        for f in fields:
            f.load()
    return load

def config(cls=None, /, *, prefix=""):
    def wrap(cls):
        fields = []
        annos = inspect.get_annotations(cls)
        for k,v in annos.items():
            fields.append(_Field(cls, k, ( prefix+k ).upper(), v, getattr(cls, k, None)))
        setattr(cls, "load", _load(fields))
        return cls
    if cls is None:
        return wrap
    return wrap(cls)
