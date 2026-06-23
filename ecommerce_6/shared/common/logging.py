"""
Shared logging configuration using structlog.
"""
import structlog
from typing import Any, Dict


def setup_logging(service_name: str, debug: bool = False) -> None:
    """Configure structured logging for a service."""
    
    log_level = "DEBUG" if debug else "INFO"
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if debug else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Get a logger instance with the given name."""
    return structlog.get_logger(name)
