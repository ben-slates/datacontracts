class Column:
    def __init__(
        self,
        dtype,
        min=None,
        max=None,
        allowed=None,
        lt=None,
        gt=None,
        between=None,
    ):
        self.dtype = dtype
        self.min = min
        self.max = max
        self.allowed = allowed
        self.lt = lt
        self.gt = gt
        self.between = between
