import logging
import os
from pathlib import Path
from typing import Optional
import win32com.client

class LibreofficeForClient:
    """A client interface for interacting with LibreOffice on Windows using COM."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initializes the LibreofficeForClient with an optional configuration path.

        Args:
            config_path (Optional[Path]): Path to the configuration file.
        """
        self.config_path = config_path
        self.libreoffice = None
        self.is_connected = False
        self.setup_logging()

    def setup_logging(self) -> None:
        """Sets up the logging configuration for the client."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("libreoffice_client.log"),
                logging.StreamHandler()
            ]
        )
        logging.info("Logging is set up.")

    def connect(self) -> bool:
        """Connects to the LibreOffice application.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        try:
            self.libreoffice = win32com.client.Dispatch("com.sun.star.ServiceManager")
            self.is_connected = True
            logging.info("Successfully connected to LibreOffice.")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to LibreOffice: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnects from the LibreOffice application."""
        if self.is_connected:
            self.libreoffice = None
            self.is_connected = False
            logging.info("Disconnected from LibreOffice.")
        else:
            logging.warning("Attempted to disconnect, but was not connected.")

    def get_version(self) -> str:
        """Retrieves the version of the connected LibreOffice application.

        Returns:
            str: The version of LibreOffice.

        Raises:
            RuntimeError: If not connected to LibreOffice.
        """
        if not self.is_connected:
            logging.error("Cannot get version, not connected to LibreOffice.")
            raise RuntimeError("Not connected to LibreOffice.")
        
        try:
            version = self.libreoffice.Version
            logging.info(f"LibreOffice version: {version}")
            return version
        except Exception as e:
            logging.error(f"Failed to get version: {e}")
            raise RuntimeError("Failed to get version from LibreOffice.")

    def is_installed(self) -> bool:
        """Checks if LibreOffice is installed on the system.

        Returns:
            bool: True if LibreOffice is installed, False otherwise.
        """
        program_files = os.environ.get("ProgramFiles", "")
        libreoffice_path = Path(program_files) / "LibreOffice" / "program" / "soffice.exe"
        installed = libreoffice_path.is_file()
        logging.info(f"LibreOffice installed: {installed}")
        return installed
