import concurrent.futures
from pathlib import Path
from typing import List, Callable, Optional
from dataclasses import dataclass
import glob
import json

@dataclass
class Result:
    path: Path
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class BatchProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_directory(self, path: Path, pattern: str = "*") -> List[Result]:
        """Process all files in a directory that match the given pattern."""
        results = []
        file_paths = list(Path(path).glob(pattern))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(self.process_file, file_path): file_path for file_path in file_paths}
            for future in concurrent.futures.as_completed(future_to_path):
                file_path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(Result(path=file_path, success=False, error=str(e)))
        
        return results

    def process_files(self, paths: List[Path], callback: Optional[Callable] = None) -> List[Result]:
        """Process a list of files with an optional callback for each processed file."""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(self.process_file, file_path): file_path for file_path in paths}
            for future in concurrent.futures.as_completed(future_to_path):
                file_path = future_to_path[future]
                try:
                    result = future.result()
                    if callback:
                        callback(result)
                    results.append(result)
                except Exception as e:
                    results.append(Result(path=file_path, success=False, error=str(e)))
        
        return results

    def process_file(self, file_path: Path) -> Result:
        """Process an individual file and return the result."""
        try:
            # Simulate file parsing (e.g., JSON parsing)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Result(path=file_path, success=True, data=data)
        except Exception as e:
            return Result(path=file_path, success=False, error=str(e))
