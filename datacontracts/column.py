class Column:
    def __init__(self, dtype, min=None, max=None, allowed=None):
        self.dtype = dtype
        self.min = min
        self.max = max
        self.allowed = allowed
