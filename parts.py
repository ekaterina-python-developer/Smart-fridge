import json
# import os
from datetime import datetime
from decimal import Decimal

CATEGORY = {
    "овощи": "кг",
    "фрукты": "кг",
    "мясо": "кг",
    "овощь": "шт",
    "фрукт": "шт",
    "жидкость": "л",
    "другое": "шт"
}


class ProductValidator:

    @staticmethod
    def validate_name(name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Название не может быть пустым")
        return name

    @staticmethod
    def validate_category(category: str) -> str:
        category = category.strip().lower()
        if category not in CATEGORY:
            raise ValueError(
                f"Недопустимая категория. Допустимые: {', '.join(CATEGORY.keys())}"
            )
        return category

    @staticmethod
    def validate_date(date: str) -> str:
        """Проверяет корректность формата даты"""
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return date
        except ValueError:
            raise ValueError("Некорректный формат даты. Используйте дд.мм.гггг")

    @staticmethod
    def validate_amount(amount_str: str) -> float:
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Количество должно быть положительным")
            return amount
        except ValueError:
            raise ValueError("Количество должно быть числом")


class Product:
    def __init__(self, name, amount, category, expiry_date):
        self.name = name
        self.amount = amount
        self.category = category
        self.expiry_date = expiry_date

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
        try:
            with open(self.data, 'r', encoding="utf-8") as file:
                data = json.load(file)
                return [Product(**item) for item in data]
        except FileNotFoundError:
            print("Файл не найден. Создан новый холодильник.")
            return []

    def _save_products(self):
        with open(self.data, 'w', encoding="utf-8") as file:
            product_written = [product.to_dict() for product in self.products]
            json.dump(product_written, file, ensure_ascii=False, indent=2)

    def add_product(self, product=Product):
        self.products.append(product)
        self._save_products()

    def delete_product(self, name, expiry_date):
        for i in range(len(self.products)):
            product = self.products[i]
            if product.name == name and product.expiry_date == expiry_date:
                del self.products[i]
                self._save_products()

    def show_all_products(self):
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

    def show_expired_products(self):
        today = datetime.now().strftime("%d.%m.%Y")
        return [p for p in self.products if p.expiry_date < today]
