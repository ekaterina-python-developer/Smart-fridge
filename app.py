"""
Главный модуль приложения для управления холодильником.

Обеспечивает взаимодействие пользователя с системой через консольный интерфейс.
"""

from parts import Fridge, Product, ProductValidator
from typing import NoReturn

def display_menu() -> None:
    """Выводит главное меню приложения."""
    print("\nМеню холодильника:")
    print("1. Добавить продукт")
    print("2. Удалить продукт")
    print("3. Показать все продукты")
    print("4. Показать количество продукта")
    print("5. Показать просроченные продукты")
    print("6. Выход")

def handle_add_product(fridge: Fridge) -> None:
    """
    Обрабатывает добавление нового продукта.

    Args:
        fridge: Экземпляр холодильника для добавления продукта
    """
    while True:
        try:
            name = ProductValidator.validate_name(input("Название: ").strip())
            category = ProductValidator.validate_category(input("Категория: ").strip())
            amount = ProductValidator.validate_amount(input("Количество: ").strip())
            expiry_date = ProductValidator.validate_date(input("Годен до (дд.мм.гггг): ").strip())

            product = Product(name, amount, category, expiry_date)
            fridge.add_product(product)
            print(f'Продукт "{name}" добавлен!')
            break
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

def handle_delete_product(fridge: Fridge) -> None:
    """
    Обрабатывает удаление продукта.

    Args:
        fridge: Экземпляр холодильника для удаления продукта
    """
    while True:
        try:
            name = ProductValidator.validate_name(input("Название: ").strip())
            expiry_date = ProductValidator.validate_date(input("Годен до (дд.мм.гггг): ").strip())

            if fridge.delete_product(name, expiry_date):
                print(f"Продукт '{name}' успешно удален!")
                break
            else:
                print(f"Продукт '{name}' с датой годности '{expiry_date}' не найден.")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

def handle_show_product_amount(fridge: Fridge) -> None:
    """
    Обрабатывает запрос количества продукта.

    Args:
        fridge: Экземпляр холодильника для поиска продукта
    """
    while True:
        try:
            name = ProductValidator.validate_name(input("Название: ").strip())
            fridge.show_product_amount(name)
            break
        except Exception as e:
            print(f"Ошибка: {e}")

def handle_show_expired_products(fridge: Fridge) -> None:
    """
    Обрабатывает запрос просроченных продуктов.

    Args:
        fridge: Экземпляр холодильника для поиска просроченных продуктов
    """
    expired = fridge.show_expired_products()
    if expired:
        for p in expired:
            print(f"Просроченные продукты: {p.name.upper()} (до {p.expiry_date})")
    else:
        print("Просроченных продуктов нет!")

def main() -> NoReturn:
    """
    Главная функция приложения.

    Реализует основной цикл работы программы и обработку пользовательского ввода.
    """
    fridge = Fridge()

    while True:
        display_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            handle_add_product(fridge)
        elif choice == "2":
            handle_delete_product(fridge)
        elif choice == "3":
            fridge.show_all_products()
        elif choice == "4":
            handle_show_product_amount(fridge)
        elif choice == "5":
            handle_show_expired_products(fridge)
        elif choice == "6":
            print("Выход из программы...")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите число от 1 до 6.")

if __name__ == '__main__':
    main()