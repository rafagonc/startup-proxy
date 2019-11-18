class NeedInheritanceException(BaseException):
    def __str__(self):
        return "Need to inherit this class to use this method"


class InvalidOptionException(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Cannot use option %s to use this factory" % self.value