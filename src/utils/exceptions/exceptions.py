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
