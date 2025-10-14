"""
Custom Exceptions for VibPath LINE Bot
Provides structured error handling across the application
"""


class VibPathException(Exception):
    """Base exception for all VibPath application errors"""

    def __init__(self, message: str, detail: str = None):
        """
        Initialize exception with message and optional detail

        Args:
            message: Human-readable error message
            detail: Additional error details for debugging
        """
        self.message = message
        self.detail = detail
        super().__init__(self.message)

    def __str__(self):
        if self.detail:
            return f"{self.message} (Detail: {self.detail})"
        return self.message


class AIAgentError(VibPathException):
    """Raised when AI agent execution fails"""
    pass


class ToolExecutionError(VibPathException):
    """Raised when AI tool execution fails"""
    pass


class SessionError(VibPathException):
    """Raised when session management fails"""
    pass


class MongoDBError(VibPathException):
    """Raised when MongoDB operations fail"""
    pass


class MongoDBConnectionError(MongoDBError):
    """Raised when MongoDB connection fails"""
    pass


class UserPreferenceError(MongoDBError):
    """Raised when user preference operations fail"""
    pass


class LINEBotError(VibPathException):
    """Raised when LINE Bot operations fail"""
    pass


class WebhookError(LINEBotError):
    """Raised when webhook processing fails"""
    pass


class ConfigurationError(VibPathException):
    """Raised when configuration is invalid or missing"""
    pass


class EnvironmentError(ConfigurationError):
    """Raised when required environment variables are missing"""
    pass
