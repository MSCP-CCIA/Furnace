class FurnaceError(Exception):
    """Base package exception."""


class ConfigurationError(FurnaceError):
    """Raised when configuration is invalid or incomplete."""


class RegistryError(FurnaceError):
    """Raised when a registry lookup fails."""
