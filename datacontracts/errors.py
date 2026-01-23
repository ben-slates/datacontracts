class ContractError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("\n".join(errors))
