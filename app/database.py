import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class Cursor:
    def __init__(self, items):
        self._items = items

    def __aiter__(self):
        self._iterator = iter(self._items)
        return self

    async def __anext__(self):
        try:
            return next(self._iterator)
        except StopIteration:
            raise StopAsyncIteration


class Collection:
    def __init__(self, name):
        self.name = name
        self.filepath = DATA_DIR / f"{name}.json"
        DATA_DIR.mkdir(exist_ok=True)
        self._data = self._load()

    def _load(self):
        if self.filepath.exists():
            with open(self.filepath) as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self._data, f, indent=2, default=str)

    def _matches(self, item, filter_dict):
        for key, value in filter_dict.items():
            if key == "$or":
                if not any(self._matches(item, clause) for clause in value):
                    return False
            elif isinstance(value, dict):
                field_value = item.get(key)
                regex_pattern = None
                regex_flags = 0
                for op, op_value in value.items():
                    if op == "$regex":
                        regex_pattern = op_value
                    elif op == "$options":
                        if "i" in op_value:
                            regex_flags = re.IGNORECASE
                    elif op == "$gte":
                        if not (field_value is not None and field_value >= op_value):
                            return False
                    elif op == "$lte":
                        if not (field_value is not None and field_value <= op_value):
                            return False
                if regex_pattern is not None:
                    if not re.search(regex_pattern, str(field_value or ""), regex_flags):
                        return False
            else:
                if item.get(key) != value:
                    return False
        return True

    async def find_one(self, filter_dict):
        for item in self._data:
            if self._matches(item, filter_dict):
                return item
        return None

    def find(self, filter_dict=None):
        if not filter_dict:
            return Cursor(self._data.copy())
        results = [item for item in self._data if self._matches(item, filter_dict)]
        return Cursor(results)

    async def insert_one(self, document):
        self._data.append(document)
        self._save()

    async def update_one(self, filter_dict, update_dict):
        for item in self._data:
            if self._matches(item, filter_dict):
                for op, fields in update_dict.items():
                    if op == "$set":
                        item.update(fields)
                    elif op == "$inc":
                        for field, amount in fields.items():
                            item[field] = item.get(field, 0) + amount
                    elif op == "$push":
                        for field, value in fields.items():
                            if field not in item:
                                item[field] = []
                            item[field].append(value)
                self._save()
                return type("Result", (), {"matched_count": 1})()
        return type("Result", (), {"matched_count": 0})()

    async def delete_one(self, filter_dict):
        for i, item in enumerate(self._data):
            if self._matches(item, filter_dict):
                del self._data[i]
                self._save()
                return type("Result", (), {"deleted_count": 1})()
        return type("Result", (), {"deleted_count": 0})()


sweets_collection = Collection("sweets")
users_collection = Collection("users")


def seed_demo_data():
    if sweets_collection._data:
        return

    demo_sweets = [
        {"_id": "sweet-1", "name": "Chocolate Cake", "category": "cake", "price": 25.99, "quantity": 50, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
        {"_id": "sweet-2", "name": "Strawberry Cupcake", "category": "cupcake", "price": 4.99, "quantity": 100, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
        {"_id": "sweet-3", "name": "Glazed Donut", "category": "donut", "price": 2.99, "quantity": 75, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
        {"_id": "sweet-4", "name": "Chocolate Chip Cookie", "category": "cookie", "price": 1.99, "quantity": 200, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
        {"_id": "sweet-5", "name": "Vanilla Ice Cream", "category": "ice cream", "price": 6.99, "quantity": 30, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
        {"_id": "sweet-6", "name": "Caramel Candy", "category": "candy", "price": 0.99, "quantity": 500, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
        {"_id": "sweet-7", "name": "Apple Pie", "category": "pie", "price": 18.99, "quantity": 3, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
        {"_id": "sweet-8", "name": "Chocolate Croissant", "category": "pastry", "price": 3.99, "quantity": 2, "creator": "demo-admin-id", "createdAt": "2025-01-01T00:00:00", "updatedAt": None},
    ]
    for sweet in demo_sweets:
        sweets_collection._data.append(sweet)
    sweets_collection._save()


seed_demo_data()
