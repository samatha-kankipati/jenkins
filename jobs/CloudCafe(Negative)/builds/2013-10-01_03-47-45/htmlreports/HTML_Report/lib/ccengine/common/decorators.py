

def attr(*args, **kwargs):
    def wrap(func):
        setattr(func, 'decorated', 1)
        for name in args:
            setattr(func, name, 1)
        func.__dict__.update(kwargs)
        return func
    return wrap
