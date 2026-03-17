from pathlib import Path
import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Metadata:
    """Dataclass representing metadata for a document."""
    title: str
    author: str
    created: str  # ISO format date string
    modified: str  # ISO format date string
    keywords: str


class LibreofficeForMetadataReader:
    """Class for reading and writing metadata for LibreOffice documents."""

    @staticmethod
    def read(path: Path) -> Metadata:
        """
        Reads metadata from a JSON file.

        Args:
            path (Path): The path to the metadata file.

        Returns:
            Metadata: An instance of the Metadata dataclass.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not a valid JSON.
            KeyError: If expected metadata fields are missing.
        """
        if not path.is_file():
            raise FileNotFoundError(f"Metadata file not found: {path}")

        with open(path, 'r', encoding='utf-8') as file:
            try:
                data: Dict[str, Any] = json.load(file)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Error parsing JSON: {e}")

            try:
                return Metadata(
                    title=data['title'],
                    author=data['author'],
                    created=data['created'],
                    modified=data['modified'],
                    keywords=data['keywords']
                )
            except KeyError as e:
                raise KeyError(f"Missing expected metadata field: {e}")

    @staticmethod
    def write(path: Path, metadata: Metadata) -> bool:
        """
        Writes metadata to a JSON file.

        Args:
            path (Path): The path to the metadata file.
            metadata (Metadata): An instance of the Metadata dataclass.

        Returns:
            bool: True if the write operation was successful, False otherwise.

        Raises:
            IOError: If there is an issue writing to the file.
        """
        data = {
            'title': metadata.title,
            'author': metadata.author,
            'created': metadata.created,
            'modified': metadata.modified,
            'keywords': metadata.keywords
        }

        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            raise IOError(f"Error writing to file: {e}")
