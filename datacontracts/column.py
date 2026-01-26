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
        nullable=False,
        autocorrect=None,  # None | "clip" | "null"
    ):
        self.dtype = dtype
        self.min = min
        self.max = max
        self.allowed = allowed
        self.lt = lt
        self.gt = gt
        self.between = between
        self.nullable = nullable
        self.autocorrect = autocorrect
