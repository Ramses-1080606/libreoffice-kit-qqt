import argparse
import json
import os
import pathlib
import csv
from dataclasses import dataclass, asdict
from typing import List, Union

@dataclass
class LibreOfficeFile:
    name: str
    path: pathlib.Path
    size: int
    modified: str

    def to_dict(self) -> dict:
        return asdict(self)

def scan_directory(directory: pathlib.Path) -> List[LibreOfficeFile]:
    """Scan the given directory for LibreOffice files and return their details."""
    if not directory.is_dir():
        raise ValueError(f"The path {directory} is not a valid directory.")
    
    files = []
    for file in directory.glob("*.odt"):
        file_info = LibreOfficeFile(
            name=file.name,
            path=file,
            size=file.stat().st_size,
            modified=file.stat().st_mtime
        )
        files.append(file_info)
    return files

def show_file_info(file: pathlib.Path) -> LibreOfficeFile:
    """Return information about a specific LibreOffice file."""
    if not file.is_file():
        raise ValueError(f"The path {file} is not a valid file.")
    
    return LibreOfficeFile(
        name=file.name,
        path=file,
        size=file.stat().st_size,
        modified=file.stat().st_mtime
    )

def export_to_json(data: List[LibreOfficeFile], output_file: pathlib.Path) -> None:
    """Export the extracted data to a JSON file."""
    with open(output_file, 'w') as json_file:
        json.dump([file.to_dict() for file in data], json_file, indent=4)

def export_to_csv(data: List[LibreOfficeFile], output_file: pathlib.Path) -> None:
    """Export the extracted data to a CSV file."""
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "path", "size", "modified"])
        writer.writeheader()
        for file in data:
            writer.writerow(file.to_dict())

def batch_process_files(files: List[pathlib.Path]) -> None:
    """Perform batch processing on multiple files."""
    for file in files:
        try:
            info = show_file_info(file)
            print(f"Processed file: {info.name}")
        except ValueError as e:
            print(f"Error processing file {file}: {e}")

def main() -> None:
    parser = argparse.ArgumentParser(description="LibreOffice for Windows Toolkit")
    subparsers = parser.add_subparsers(dest='command')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan directory for LibreOffice files')
    scan_parser.add_argument('directory', type=str, help='Directory to scan')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show information about a specific file')
    info_parser.add_argument('file', type=str, help='Path to the LibreOffice file')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to JSON/CSV')
    export_parser.add_argument('format', choices=['json', 'csv'], help='Format for export')
    export_parser.add_argument('output', type=str, help='Output file path')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process multiple files')
    batch_parser.add_argument('files', type=str, nargs='+', help='List of files to process')

    args = parser.parse_args()

    try:
        if args.command == 'scan':
            directory = pathlib.Path(args.directory)
            files = scan_directory(directory)
            for file in files:
                print(file.to_dict())

        elif args.command == 'info':
            file_path = pathlib.Path(args.file)
            file_info = show_file_info(file_path)
            print(file_info.to_dict())

        elif args.command == 'export':
            directory = pathlib.Path('.')
            files = scan_directory(directory)
            if args.format == 'json':
                export_to_json(files, pathlib.Path(args.output))
            elif args.format == 'csv':
                export_to_csv(files, pathlib.Path(args.output))

        elif args.command == 'batch':
            file_paths = [pathlib.Path(file) for file in args.files]
            batch_process_files(file_paths)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
