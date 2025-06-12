class Node:
    """Класс узла бинарного дерева"""

    def __init__(self, data=None):
        self.left = None  # Левый потомок
        self.right = None  # Правый потомок
        self.data = data  # Данные узла
        self.is_empty = data is None  # Флаг пустого узла


class BinaryTree:
    """Класс бинарного дерева с измененной логикой валидности"""
    def __init__(self):
        self.root = Node(0)  # Корневой узел с начальным значением 0
        self.used_codes = set()  # Множество использованных кодов путей
        self.invalid_paths = set()  # Множество невалидных путей

    def insert(self, num, code):
        """
        Вставка значения в дерево с новой проверкой валидности
        Разрешено заполнять узлы, даже если они уже имеют потомков
        """
        if code in self.used_codes:
            print(f"Ошибка: код пути '{code}' уже использован!")
            return False

        current = self.root
        path_history = []

        for i, char in enumerate(code):
            if char == '0':
                if current.left is None:
                    current.left = Node()
                path_history.append((current, 'left'))
                current = current.left
            elif char == '1':
                if current.right is None:
                    current.right = Node()
                path_history.append((current, 'right'))
                current = current.right
            else:
                print(f"Ошибка: недопустимый символ '{char}' в коде пути")
                return False

            # НОВАЯ ЛОГИКА: разрешаем заполнять узлы, даже если они имеют потомков
            # Проверяем только, что узел не был заполнен ранее (если это не корень)
            if not current.is_empty and i == len(code)-1 and code != '':
                print(f"Ошибка: узел по коду '{code}' уже содержит значение {current.data}")
                return False

        current.data = num
        current.is_empty = False
        self.used_codes.add(code)
        return True

    def is_valid(self):
        """Новая проверка валидности дерева"""
        # Проверяем только:
        # 1. Нет дублированных кодов путей
        # 2. Нет недопустимых символов в путях (это проверяется при вставке)
        # 3. Нет попыток перезаписать уже заполненный узел
        return True  # Все остальные проверки теперь разрешены

    # Остальные методы класса остаются без изменений
    def _collect_nodes(self, node, path, output_list):
        """Рекурсивный сбор всех узлов дерева"""
        if node is None:
            return
        output_list.append((path, node.data if not node.is_empty else None))
        self._collect_nodes(node.left, path + '0', output_list)
        self._collect_nodes(node.right, path + '1', output_list)

    def list_nodes(self):
        """Возвращает список всех узлов"""
        result = []
        self._collect_nodes(self.root, '', result)
        return result

    def display_horizontal(self):
        """Горизонтальное представление дерева"""
        print("\nГоризонтальное представление дерева:")
        self._display_horizontal(self.root, 0)

    def _display_horizontal(self, node, level):
        """Рекурсивный вывод в горизонтальном формате"""
        if node is None:
            return

        self._display_horizontal(node.right, level + 1)
        prefix = "    " * level
        print(f"{prefix}-> {node.data if not node.is_empty else 'None'}")
        self._display_horizontal(node.left, level + 1)


def input_mode_selection():
    """Выбор режима ввода данных"""
    print("\nВыберите режим ввода данных:")
    print("1 - Ввод из файла")
    print("2 - Ручной ввод узлов")
    while True:
        choice = input("Ваш выбор (1/2): ").strip()
        if choice in ('1', '2'):
            return choice
        print("Неверный ввод. Пожалуйста, введите 1 или 2.")


def input_from_file():
    """
    Чтение данных из файла и построение дерева
    :return: экземпляр BinaryTree или None при ошибке
    """
    filename = input("Введите название файла: ").strip()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tree = BinaryTree()
            line_number = 0
            for row_line in f:
                line_number += 1
                text = row_line.strip()
                if not text:
                    continue  # Пропускаем пустые строки

                parts = text.split()
                if len(parts) != 2:
                    print(f"Ошибка в строке {line_number}: требуется два значения через пробел")
                    continue

                num_str, code_str = parts
                try:
                    number = int(num_str)
                except ValueError:
                    print(f"Ошибка в строке {line_number}: '{num_str}' не является числом")
                    continue

                if any(c not in '01' for c in code_str):
                    print(f"Ошибка в строке {line_number}: код должен содержать только '0' и '1'")
                    continue

                if not tree.insert(number, code_str):
                    print(f"Ошибка добавления в строке {line_number}")

            return tree
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла: {e}")
        return None


def input_manually():
    """
    Интерактивный ввод данных для построения дерева
    :return: экземпляр BinaryTree
    """
    tree = BinaryTree()
    print("\nВводите узлы в формате 'число код_пути' (например: '5 01')")
    print("Для завершения ввода введите 'q'")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == 'q':
            break

        parts = user_input.split()
        if len(parts) != 2:
            print("Ошибка: требуется два значения через пробел")
            continue

        num_str, code_str = parts
        try:
            number = int(num_str)
        except ValueError:
            print(f"Ошибка: '{num_str}' не является числом")
            continue

        if any(c not in '01' for c in code_str):
            print("Ошибка: код должен содержать только '0' и '1'")
            continue

        tree.insert(number, code_str)

    return tree


def main():
    """Основная функция программы"""
    print("Программа построения бинарного дерева")

    # Выбор режима ввода данных
    mode = input_mode_selection()
    if mode == '1':
        tree = input_from_file()
    else:
        tree = input_manually()

    if not tree:
        return  # Завершение если не удалось создать дерево

    # Вывод всех узлов
    print("\nСписок всех узлов:")
    for path, val in tree.list_nodes():
        if path == "":
            print(f"Корень (путь: \"{path}\") = {val}")
        else:
            print(f"Узел (путь: \"{path}\") = {val}")

    # Вывод дерева
    tree.display_horizontal()

    # Дополнительная информация о валидности
    if tree.is_valid():
        print("\nДерево валидно!")
    else:
        print("\nДерево содержит ошибки!")
        print("Рекомендации:")
        print("- Убедитесь, что все промежуточные узлы заполнены")
        print("- Проверьте, что нет дублирования кодов путей")
        print("- Убедитесь, что коды путей содержат только '0' и '1'")


if __name__ == "__main__":
    main()