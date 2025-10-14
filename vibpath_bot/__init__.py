"""
VibPath LINE Bot Package
========================

Professional frequency therapy LINE Bot implementation.

Modules:
    templates/: Flex Message templates and UI components
    handlers/: Message and event handlers
    config/: Configuration management
    utils/: Utility functions and helpers
"""

__version__ = "1.0.0"
__author__ = "VibPath"

# Lazy imports - components will be imported when needed
__all__ = [
    "MessageHandler",
    "button_config_manager"
]