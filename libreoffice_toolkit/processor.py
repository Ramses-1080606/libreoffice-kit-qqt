from pathlib import Path
from typing import Dict, Any, List, Callable
import json
import os

class LibreofficeForProcessor:
    def __init__(self, client: 'LibreofficeForClient'):
        """
        Initializes the processor with a LibreOffice client.

        :param client: An instance of LibreofficeForClient to interact with LibreOffice.
        """
        self.client = client

    def process_file(self, path: Path) -> Dict[str, Any]:
        """
        Processes a single file to extract text and metadata.

        :param path: Path to the file to be processed.
        :return: A dictionary with extracted text and metadata.
        """
        try:
            text = self.extract_text(path)
            metadata = self.extract_metadata(path)
            return {
                'text': text,
                'metadata': metadata
            }
        except Exception as e:
            print(f"Error processing file {path}: {e}")
            return {}

    def extract_text(self, path: Path) -> str:
        """
        Extracts text from a LibreOffice document.

        :param path: Path to the document file.
        :return: Extracted text as a string.
        """
        if not path.exists():
            raise FileNotFoundError(f"The specified file does not exist: {path}")

        # Simulate text extraction (actual extraction logic would depend on the client)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()  # Simplified for demonstration
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from {path}: {e}")

    def extract_metadata(self, path: Path) -> Dict:
        """
        Extracts metadata from a LibreOffice document.

        :param path: Path to the document file.
        :return: A dictionary containing metadata.
        """
        if not path.exists():
            raise FileNotFoundError(f"The specified file does not exist: {path}")

        # Simulate metadata extraction
        try:
            metadata = {
                'filename': path.name,
                'size': os.path.getsize(path),
                'last_modified': os.path.getmtime(path)
            }
            return metadata
        except Exception as e:
            raise RuntimeError(f"Failed to extract metadata from {path}: {e}")

    def batch_process(self, paths: List[Path], progress_callback: Callable[[int], None] = None) -> List[Dict]:
        """
        Processes a batch of files and calls a progress callback.

        :param paths: List of paths to files to be processed.
        :param progress_callback: A callback function to report progress.
        :return: A list of results for each processed file.
        """
        results = []
        total_files = len(paths)

        for index, path in enumerate(paths):
            result = self.process_file(path)
            results.append(result)
            if progress_callback:
                progress_callback((index + 1) / total_files)

        return results
