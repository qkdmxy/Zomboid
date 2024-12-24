class ConsolePrinter:
    def __init__(self, data: list[dict[str, str | int]]):
        self.data = data

    def print_all(self) -> None:
        if not self.data:
            print("No data available to print.")
            return
        for item in self.data:
            print(f"ID: {item['id']}, Name: {item['name']}, "
                  f"Type: {item['type']}, Condition: {item['condition']}, "
                  f"Amount: {item['amount']}")

    def print_paginated(self, page: int, items_per_page: int = 10) -> None:
        if not self.data:
            print("No data available to print.")
            return
        start = (page - 1) * items_per_page
        end = start + items_per_page
        if start >= len(self.data):
            print(f"Page {page} is out of range. There are only {len(self.data) // items_per_page + 1} pages available.")
            return
        for item in self.data[start:end]:
            print(f"ID: {item['id']}, Name: {item['name']}, "
                  f"Type: {item['type']}, Condition: {item['condition']}, "
                  f"Amount: {item['amount']}")