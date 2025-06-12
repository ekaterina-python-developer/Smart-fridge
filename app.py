from parts import Fridge, Product


def main():
    fridge = Fridge()

    while True:
        print("1. Добавить продукт")
        print("2. Удалить продукт")
        print("3. Показать все продукты")
        print("4. Показать количество продукта")
        print("5. Показать просроченные продукты")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Название: ")
            category = input("Категория: ")
            amount = input("Количество: ")
            expiry_date = input("Годен до (дд.мм.гггг): ")
            fridge.add_product(Product(name, amount, category, expiry_date))
            print(f'Продукт {name} добавлен!')

        if choice == "2":
            name = input("Введите название продукта для удаления: ").strip()
            expiry_date = input("Введите срок годности продукта (дд.мм.гггг): ").strip()
            fridge.delet_product(name, expiry_date)
            print(f'Продукт {name} удален!')

        if choice == "3":
            print(fridge.show_all_product())
            break

        if choice == "4":
            name = input("Введите название продукта: ").strip()
            fridge.show_product_amount(name)
            break

        if choice == "5":
            expired = fridge.show_expiry_product()
            if expired:
                for p in expired:
                    print(f"Просроченные продукты: {str.upper(p.name)} (до {p.expiry_date})")
            else:
                print("Просрочки нет!")
            break

        if choice == "6":
            break


if __name__ == '__main__':
    main()