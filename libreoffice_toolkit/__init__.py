"""
LibreOffice for Windows Toolkit - Python automation and utilities

A comprehensive toolkit for working with LibreOffice for Windows files and automation.
"""
from .client import LibreofficeForClient
from .processor import LibreofficeForProcessor
from .metadata import LibreofficeForMetadataReader
from .batch import BatchProcessor
from .exporter import DataExporter

__version__ = "0.1.0"
__author__ = "Open Source Community"

__all__ = [
    "LibreofficeForClient",
    "LibreofficeForProcessor",
    "LibreofficeForMetadataReader",
    "BatchProcessor",
    "DataExporter",
]
