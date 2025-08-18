class ValidationException(Exception):
    def __init__(self, value: str):
        self.value = value


class ValidationsException(Exception):
    def __init__(self, invalid: dict, valid: dict):
        self.valid = valid
        self.invalid = invalid
