class NotInElastic(BaseException):
    message = "nothing to delete"


class NoIndex(BaseException):
    message = "index not in elastic"
