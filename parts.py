"""
Модуль для управления содержимым холодильника.

Содержит классы для работы с продуктами, их валидации и хранения в JSON-файле.
Реализовано кеширование часто запрашиваемых данных для оптимизации производительности.
"""

import json
from datetime import datetime
from decimal import Decimal
from functools import lru_cache
from typing import List, Dict, Union, Optional

# Константы модуля
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
    """
    Класс для валидации данных о продуктах.

    Реализует статические методы проверки корректности вводимых данных.
    """

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Проверяет валидность названия продукта.

        Args:
            name: Название продукта для проверки

        Returns:
            Очищенное название продукта

        Raises:
            ValueError: Если название пустое
        """
        name = name.strip()
        if not name:
            raise ValueError("Название не может быть пустым")
        return name

    @staticmethod
    def validate_category(category: str) -> str:
        """
        Проверяет валидность категории продукта.

        Args:
            category: Категория для проверки

        Returns:
            Очищенная и приведенная к нижнему регистру категория

        Raises:
            ValueError: Если категория недопустима
        """
        category = category.strip().lower()
        if category not in CATEGORY:
            raise ValueError(
                f"Недопустимая категория. Допустимые: {', '.join(CATEGORY.keys())}"
            )
        return category

    @staticmethod
    def validate_date(date: str) -> str:
        """
        Проверяет корректность формата даты.

        Args:
            date: Дата в формате 'дд.мм.гггг'

        Returns:
            Переданную дату, если она валидна

        Raises:
            ValueError: Если формат даты некорректен
        """
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return date
        except ValueError:
            raise ValueError("Некорректный формат даты. Используйте дд.мм.гггг")

    @staticmethod
    def validate_amount(amount_str: str) -> float:
        """
        Проверяет валидность количества продукта.

        Args:
            amount_str: Количество в виде строки

        Returns:
            Количество в виде float

        Raises:
            ValueError: Если количество не число или <= 0
        """
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Количество должно быть положительным")
            return amount
        except ValueError:
            raise ValueError("Количество должно быть числом")


class Product:
    """
    Класс, представляющий продукт в холодильнике.

    Attributes:
        name (str): Название продукта
        amount (float): Количество продукта
        category (str): Категория продукта
        expiry_date (str): Дата годности в формате 'дд.мм.гггг'
    """

    def __init__(self, name: str, amount: float, category: str, expiry_date: str):
        """
        Инициализирует новый продукт.

        Args:
            name: Название продукта
            amount: Количество продукта
            category: Категория продукта
            expiry_date: Дата годности в формате 'дд.мм.гггг'
        """
        self.name = name
        self.amount = amount
        self.category = category
        self.expiry_date = expiry_date

    def to_dict(self) -> Dict[str, Union[str, float]]:
        """
        Преобразует продукт в словарь для сериализации.

        Returns:
            Словарь с атрибутами продукта
        """
        return {
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "expiry_date": self.expiry_date,
        }


class Fridge:
    """
    Класс для управления содержимым холодильника.

    Обеспечивает:
    - Загрузку/сохранение продуктов в JSON-файл
    - Добавление/удаление продуктов
    - Поиск и анализ продуктов
    - Кеширование часто запрашиваемых данных
    """

    def __init__(self, filename: str = 'storage.json'):
        """
        Инициализирует холодильник с указанным файлом хранилища.

        Args:
            filename: Путь к файлу хранилища (по умолчанию 'storage.json')
        """
        self.data = filename
        self.products = self._load_products()

    def _load_products(self) -> List[Product]:
        """
        Загружает продукты из файла хранилища.

        Returns:
            Список загруженных продуктов

        Note:
            При ошибках загрузки возвращает пустой список
        """
        try:
            with open(self.data, 'r', encoding="utf-8") as file:
                data = json.load(file)
                return [Product(**item) for item in data]
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка загрузки данных: {e}. Создан новый список продуктов.")
            return []

    def _save_products(self) -> None:
        """
        Сохраняет текущий список продуктов в файл хранилища.

        Note:
            При ошибках сохранения выводит сообщение в консоль
        """
        try:
            with open(self.data, 'w', encoding="utf-8") as file:
                product_written = [product.to_dict() for product in self.products]
                json.dump(product_written, file, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения данных: {e}")

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в холодильник.

        Args:
            product: Продукт для добавления

        Note:
            Автоматически очищает кеш количества продуктов
        """
        self.products.append(product)
        self._save_products()
        self.show_product_amount.cache_clear()

    def delete_product(self, name: str, expiry_date: str) -> bool:
        """
        Удаляет продукт из холодильника.

        Args:
            name: Название продукта
            expiry_date: Дата годности продукта

        Returns:
            True если продукт был удален, иначе False

        Note:
            Автоматически очищает кеш количества продуктов
        """
        for i in range(len(self.products) - 1, -1, -1):
            product = self.products[i]
            if product.name == name and product.expiry_date == expiry_date:
                del self.products[i]
                self._save_products()
                self.show_product_amount.cache_clear()
                return True
        return False

    def show_all_products(self) -> None:
        """Выводит в консоль список всех продуктов в холодильнике."""
        if self.products:
            for p in self.products:
                print(f"{p.name} | Категория: {p.category} | Годен до: {p.expiry_date}")
        else:
            print("Холодильник пуст!")

    @lru_cache(maxsize=32)
    def show_product_amount(self, name: str) -> str:
        """
        Возвращает общее количество указанного продукта.

        Args:
            name: Название продукта

        Returns:
            Строка с информацией о количестве продукта

        Note:
            Результаты кешируются для оптимизации
        """
        total = Decimal('0')
        found = False

        for p in self.products:
            if p.name == name:
                total += Decimal(str(p.amount))
                unit = CATEGORY.get(p.category, "шт")
                found = True

        if found:
            msg = f'Продукта "{name}": {float(total)} {unit}'
            print(msg)
            return msg
        else:
            msg = f'Продукт "{name}" не найден.'
            print(msg)
            return msg

    def show_expired_products(self) -> List[Product]:
        """
        Возвращает список просроченных продуктов.

        Returns:
            Список продуктов с истекшим сроком годности
        """
        today = datetime.now().strftime("%d.%m.%Y")
        return [p for p in self.products if p.expiry_date < today]
