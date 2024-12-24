import json
import csv
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union


class AbstractReader(ABC):
    def __init__(self, path: Path):
        self.file_path = path

    @abstractmethod
    def read(self) -> List[Dict[str, Union[str, int]]]:
        pass


class FileReader(AbstractReader):
    def __init__(self, path: Path):
        super().__init__(path)
        self.data: List[Dict[str, Union[str, int]]] = []

    def _convert_value(self, value: str) -> Union[str, int]:
        try:
            return int(value)
        except ValueError:
            return value


class CSVFileReader(FileReader):
    def read(self) -> List[Dict[str, Union[str, int]]]:
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    normalized_row = {
                        key.lower(): self._convert_value(value) for key, value in row.items()
                    }
                    self.data.append(normalized_row)
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        return self.data


class JSONFileReader(FileReader):
    def read(self) -> List[Dict[str, Union[str, int]]]:
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                loaded_data = json.load(file)
                if not isinstance(loaded_data, list):
                    raise ValueError("The JSON file must contain a list of objects.")
                for entry in loaded_data:
                    if isinstance(entry, dict) and all(isinstance(v, (str, int)) for v in entry.values()):
                        normalized_entry = {key.lower(): value for key, value in entry.items()}
                        self.data.append(normalized_entry)
                    else:
                        raise ValueError("JSON entries must be dictionaries with string or integer values.")
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            print(f"File {self.file_path} contains invalid JSON.")
        except Exception as e:
            print(f"Error reading JSON file: {e}")
        return self.data