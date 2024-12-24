import os
import json
import csv
from typing import List, Dict
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET


class FileProcessor:
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self) -> List[Dict]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"File '{self.file_path}' does not exist.")
        
        if self.file_path.suffix == ".json":
            return self._load_json()
        elif self.file_path.suffix == ".csv":
            return self._load_csv()
        elif self.file_path.suffix == ".xml":
            return self._load_xml()
        else:
            raise ValueError(f"Unsupported file format: {self.file_path.suffix}")

    def _load_json(self) -> List[Dict]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _load_csv(self) -> List[Dict]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def _load_xml(self) -> List[Dict]:
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return [{child.tag: child.text for child in element} for element in root]


class DataAnalyzer:
    
    def __init__(self, data: List[Dict]):
        self.data = data

    def calculate_condition_percentages(self, filter_name: str = None) -> Dict[str, float]:
        filtered_data = [item for item in self.data if not filter_name or item.get("name") == filter_name]
        total_items = len(filtered_data)
        
        if total_items == 0:
            return {}

        condition_counts = {}
        for item in filtered_data:
            condition = item.get("condition")
            condition_counts[condition] = condition_counts.get(condition, 0) + 1

        return {condition: (count / total_items) * 100 for condition, count in condition_counts.items()}


def display_results(results: Dict[str, float], filter_name: str = None):
    if filter_name:
        print(f"Condition percentages for items named '{filter_name}':")
    else:
        print("Condition percentages for all items:")
    
    for condition, percentage in results.items():
        print(f"{condition}: {percentage:.2f}%")


def main():
    parser = argparse.ArgumentParser(description="Analyze data from a file.")
    parser.add_argument("file_path", type=Path, help="Path to the file (JSON, CSV, XML).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--percentage-all", action="store_true", help="Show condition percentages for all items.")
    group.add_argument("--percentage-name", type=str, help="Show condition percentages for items with the specified name.")

    args = parser.parse_args()

    try:
        file_processor = FileProcessor(args.file_path)
        analyzer = DataAnalyzer(file_processor.data)

        if args.percentage_all:
            results = analyzer.calculate_condition_percentages()
            display_results(results)

        if args.percentage_name:
            results = analyzer.calculate_condition_percentages(args.percentage_name)
            display_results(results, args.percentage_name)

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        exit(1)

if __name__ == "__main__":
    main()