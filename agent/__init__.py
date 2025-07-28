
"""Restaceratops – Async API‑testing agent."""
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("restaceratops")
except PackageNotFoundError:
    __version__ = "0.1.0"
