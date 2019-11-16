class DatabaseException(Exception):
    pass


class UserAlreadyExistsException(DatabaseException):
    pass


class UserIsNotExistException(DatabaseException):
    pass


class WishListItemIsNotExistException(DatabaseException):
    pass


class ItemIsNotExistException(DatabaseException):
    pass


class ChallengeIsNotExistException(DatabaseException):
    pass


class SubCategoryIsNotExistException(DatabaseException):
    pass


class CategoryIsNotExistException(DatabaseException):
    pass
