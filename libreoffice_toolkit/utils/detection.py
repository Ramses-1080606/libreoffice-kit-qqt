import os
import subprocess
from pathlib import Path
from typing import Optional

def find_installation() -> Optional[Path]:
    """
    Check common installation paths for LibreOffice on Windows.

    Returns:
        Optional[Path]: The path to the LibreOffice installation directory if found, otherwise None.
    """
    common_paths = [
        Path("C:/Program Files/LibreOffice/program"),
        Path("C:/Program Files (x86)/LibreOffice/program"),
        Path("D:/Program Files/LibreOffice/program"),
        Path("D:/Program Files (x86)/LibreOffice/program"),
    ]
    
    for path in common_paths:
        if path.exists() and path.is_dir():
            return path
    return None

def get_version() -> Optional[str]:
    """
    Get the version of the installed LibreOffice.

    Returns:
        Optional[str]: The version string if LibreOffice is installed, otherwise None.
    """
    installation_path = find_installation()
    if installation_path:
        version_file = installation_path / "soffice.exe"
        try:
            result = subprocess.run([str(version_file), "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            print(f"Error while retrieving LibreOffice version: {e}")
    return None

def is_installed() -> bool:
    """
    Check if LibreOffice is installed on the system.

    Returns:
        bool: True if LibreOffice is installed, otherwise False.
    """
    return find_installation() is not None

def get_executable_path() -> Optional[Path]:
    """
    Get the path to the LibreOffice executable.

    Returns:
        Optional[Path]: The path to the LibreOffice executable if found, otherwise None.
    """
    installation_path = find_installation()
    if installation_path:
        return installation_path / "soffice.exe"
    return None
