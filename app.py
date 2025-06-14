
from parts import Fridge, Product, ProductValidator


def main():
    fridge = Fridge()

    while True:
        print("\nМеню холодильника:")
        print("1. Добавить продукт")
        print("2. Удалить продукт")
        print("3. Показать все продукты")
        print("4. Показать количество продукта")
        print("5. Показать просроченные продукты")
        print("6. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            while True:
                try:
                    name = ProductValidator.validate_name(
                        input("Название: ").strip()
                    )
                    category = ProductValidator.validate_category(
                        input("Категория: ").strip()
                    )
                    amount = ProductValidator.validate_amount(
                        input("Количество: ").strip()
                    )
                    expiry_date = ProductValidator.validate_date(
                        input("Годен до (дд.мм.гггг): ").strip()
                    )

                    product = Product(name, amount, category, expiry_date)
                    fridge.add_product(product)
                    print(f'Продукт "{name}" добавлен!')
                    break
                except ValueError as e:
                    print(f"Ошибка ввода: {e}")
                except Exception as e:
                    print(f"Неожиданная ошибка: {e}")

        elif choice == "2":
            while True:
                try:
                    name = ProductValidator.validate_name(
                        input("Название: ").strip()
                    )
                    expiry_date = ProductValidator.validate_date(
                        input("Годен до (дд.мм.гггг): ").strip()
                    )
                    if fridge.delete_product(name, expiry_date):
                        print(f"Продукт '{name}' успешно удален!")
                        break
                    else:
                        print(f"Продукт '{name}' с датой годности '{expiry_date}' не найден.")
                except ValueError as e:
                    print(f"Ошибка ввода: {e}")
                except Exception as e:
                    print(f"Неожиданная ошибка: {e}")

        elif choice == "3":
            fridge.show_all_products()

        elif choice == "4":
            while True:
                try:
                    name = ProductValidator.validate_name(
                        input("Название: ").strip()
                    )
                    fridge.show_product_amount(name)
                    break
                except Exception as e:
                    print(f"Ошибка: {e}")
            break

        elif choice == "5":
            expired = fridge.show_expired_products()
            if expired:
                for p in expired:
                    print(f"Просроченные продукты: {str.upper(p.name)} (до {p.expiry_date})")
            else:
                print("Просроченных продуктов нет!")
            break

        elif choice == "6":
            print("Выход из программы...")
            break

        else:
            print("Некорректный выбор. Пожалуйста, введите число от 1 до 6.")


if __name__ == '__main__':
    main()