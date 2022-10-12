from werkzeug.exceptions import BadRequest, NotFound


class OwnerAlreadyHasThreeCars(BadRequest):
    def __init__(self):
        super().__init__()
        self.message = "The selected owner already has three cars."


class ObjectNotFound(NotFound):
    def __init__(self):
        super().__init__()
        self.message = "The object was not found."


class OwnerStillHasACar(BadRequest):
    def __init__(self):
        super().__init__()
        self.message = "The defined owner can't be deleted because he still has a car."
