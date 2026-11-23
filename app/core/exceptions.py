from sqlalchemy.exc import IntegrityError

class AlreadyExistsError(Exception):
    pass

class NonexistingError(Exception):
    pass

class IncorrectPassword(Exception):
    pass

def violates_unique(error: IntegrityError, constraint: str):
    original = error.orig
    driver_error = getattr(original, "__cause__", None)
    return (
        getattr(original, "sqlstate", None) == "23505"
        and getattr(driver_error, "constraint_name", None) == constraint
    )
    