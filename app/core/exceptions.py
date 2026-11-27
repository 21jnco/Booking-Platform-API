from sqlalchemy.exc import IntegrityError

class AlreadyExistsError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class NonexistingError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class IncorrectData(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

def violates_unique(error: IntegrityError, constraint: str):
    original = error.orig
    driver_error = getattr(original, "__cause__", None)
    return (
        getattr(original, "sqlstate", None) == "23505"
        and getattr(driver_error, "constraint_name", None) == constraint
    )
    