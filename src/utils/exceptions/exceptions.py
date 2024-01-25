class InvalidUsernameOrPasswordException(Exception):
    pass


class AlreadyExistsException(Exception):
    pass


class InvalidCustomerIDException(Exception):
    pass


class InvalidEmployeeIDException(Exception):
    pass


class InvalidDepartmentIDException(Exception):
    pass


class NoDepartmentsException(Exception):
    pass


class CustomerTicketIDMismatchException(Exception):
    pass


class NoFeedbackExistsException(Exception):
    pass


class NoMessageFromHelpdeskException(Exception):
    pass


class NoTicketsException(Exception):
    pass


class NoMessageFromManagerException(Exception):
    pass


class DataBaseException(Exception):
    pass


class ApplicationError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
    
