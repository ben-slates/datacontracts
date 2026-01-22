class ContractError(Exception):
    def __init__(self, errors):
        self.errors = errors
        message = "\n".join(errors)
        super().__init__(message)
