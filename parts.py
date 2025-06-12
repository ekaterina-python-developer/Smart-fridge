import json
import os
from datetime import datetime
from decimal import Decimal

CATEGORY = {
    "овощи": "кг",
    "фрукты": "кг",
    "мясо": "кг",
    "жидкость": "л"
}


class Product:
    def __init__(self, name, amount, category, expiry_date):
        self.name = name
        self.amount = amount
        self.category = category
        self.expiry_date = self._validate_date(expiry_date)

    @staticmethod
    def _validate_date(date: str) -> str:
        """Проверяет корректность формата даты"""
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return date
        except ValueError:
            raise ValueError("Некорректный формат даты. Используйте дд.мм.гггг")

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "expiry_date": self.expiry_date,
        }


class Fridge:
    def __init__(self):
        self.data = 'storage.json'
        self.products = self._load_products()

    def _load_products(self):
        if os.path.exists(self.data):
            with open(self.data, 'r', encoding="utf-8") as file:
                products_load = json.load(file)
                return [Product(**item) for item in products_load]
        return []

    def _save_products(self):
        with open(self.data, 'w', encoding="utf-8") as file:
            product_written = [product.to_dict() for product in self.products]
            json.dump(product_written, file, ensure_ascii=False, indent=2)

    def add_product(self, product=Product):
        self.products.append(product)
        self._save_products()

    def delet_product(self, name, expiry_date):
        for i in range(len(self.products)):
            product = self.products[i]
            if product.name == name and product.expiry_date == expiry_date:
                del self.products[i]
                self._save_products()

    def show_all_product(self):
        for p in self.products:
            print(f"{p.name} | Категория: {p.category} | Годен до: {p.expiry_date}")

    def show_product_amount(self, name):
        total = 0
        for p in self.products:
            if p.name == name:
                total += Decimal(p.amount)
                unit = CATEGORY.get(p.category, "шт")

        if total > 0:
            print(f'Продукта "{name}": {total} {unit}')
        else:
            print(f'Продукт с именем "{name}" не найден.')

    def show_expiry_product(self):
        today = datetime.now().strftime("%d.%m.%Y")
        return [p for p in self.products if p.expiry_date < today]
