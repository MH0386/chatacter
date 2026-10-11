class Error(Exception):
    """Base class for all chatacter exceptions."""


class InvalidArgumentError(Error):
    """Raised when an invalid argument is passed to a function."""


class DocumentIndexingError(Error):
    """Raised when a document cannot be indexed into a File Search store."""
