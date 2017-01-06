class UserError(Exception):
    def __init__(self,message):
        self.message=message


class UserNotExists(UserError): ##Inheritance
    pass


class IncorrectPassword(UserError):##Direct Inheritance
    pass

class UserAlreadyExists(UserError):
    pass

class EmailInvalid(UserError):
    pass
