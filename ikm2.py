"""
Программа для построения двоичного дерева по кодам путей.
Коды путей представляют собой последовательности из 0 (левый потомок) и 1 (правый потомок).
"""

class Node:
    """Класс узла двоичного дерева"""

    def __init__(self, data=None):
        self.data = data    # Значение узла
        self.left = None    # Левый потомок
        self.right = None   # Правый потомок


class TreeManager:
    """Класс для управления двоичным деревом и операциями с ним"""

    def __init__(self):
        """Инициализация дерева с корневым узлом (значение 0)"""
        self.root = Node(0)


    def ensure_path(self, node, code, prompt_intermediate, prompt_final, final_value=None):
        """
        Создает путь в дереве по заданному коду.
        Args:
            node: текущий узел
            code: оставшаяся часть кода пути
            prompt_intermediate: запрашивать ли значения для промежуточных узлов
            prompt_final: запрашивать ли значения для конечных узлов
            final_value: значение для установки в конечном узле (если указано)
        Returns:
            Созданный/найденный конечный узел
        """
        if not code:
            if final_value is not None:
                node.data = final_value
            return node

        branch = 'left' if code[0] == '0' else 'right'
        child = getattr(node, branch)

        if child is None:
            if (len(code) > 1 and prompt_intermediate) or (len(code) == 1 and prompt_final):
                child = self._create_node_with_prompt(code)
            else:
                child = Node()
            setattr(node, branch, child)

        return self.ensure_path(child, code[1:], prompt_intermediate, prompt_final, final_value)


    def _create_node_with_prompt(self, code):
        """Запрашивает у пользователя значение для нового узла"""
        while True:
            text = input(
                f"Введите целое для {'промежуточного' if len(code) > 1 else 'конечного'} узла '{code[0]}' (от '{code}'): ").strip()
            if text.isdigit():
                return Node(int(text))
            print("Ошибка: нужно целое неотрицательное число.")


    def collect_nodes(self, node, path="", out=None):
        """
        Собирает все узлы дерева с их путями и значениями.
        Args:
            node: текущий узел
            path: текущий путь от корня
            out: список для сбора результатов
        Returns:
            Список кортежей (путь, значение)
        """
        if out is None:
            out = []
        out.append((path, node.data))
        if node.left:
            self.collect_nodes(node.left, path + "0", out)
        if node.right:
            self.collect_nodes(node.right, path + "1", out)
        return out


    def print_all(self):
        """Выводит полную информацию о дереве"""
        print("\nСписок узлов (код путь : значение):")
        for path, val in self.collect_nodes(self.root):
            print(f"{path or 'root':>5} : {val}")

        print("\nГоризонтальное представление дерева:")
        self._print_tree(self.root)


    def _print_tree(self, node, level=0):
        """
        Рекурсивно печатает дерево в горизонтальном формате.
        Args:
            node: текущий узел
            level: текущий уровень вложенности
        """
        if node.right:
            self._print_tree(node.right, level + 1)
        print("    " * level + f"-> {node.data}")
        if node.left:
            self._print_tree(node.left, level + 1)


class InputHandler:
    """Класс для обработки входных данных (из файла или ручного ввода)"""

    def __init__(self):
        self.entries = []  # Список пар (число, код)
        self.seen_codes = set()  # Множество для отслеживания уникальных кодов

    def process_file(self, filename):
        """
        Читает и обрабатывает данные из файла.
        Args:
            filename: имя файла для чтения
        Returns:
            Отсортированный список входных данных или None при ошибке
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for lineno, line in enumerate(f, 1):
                    self._process_line(line, lineno)
            return self._sort_entries()
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            return None

    def process_manual_input(self):
        """Обрабатывает ручной ввод данных пользователем"""
        print("Ручной ввод. Формат: <число> <код 0/1>, 'q' — выход.")
        while True:
            s = input("> ").strip()
            if s.lower() == 'q':
                break
            self._process_line(s)
        return self._sort_entries()

    def _process_line(self, line, lineno=None):
        """
        Парсит одну строку входных данных.

        Args:
            line: строка для обработки
            lineno: номер строки (для сообщений об ошибках)
        """
        text = line.strip()
        if not text:
            return
        parts = text.split()
        if len(parts) != 2 or not parts[0].isdigit() or any(ch not in '01' for ch in parts[1]):
            if lineno:
                print(f"[Строка {lineno}] Пропущена: ожидается '<число> <код>'.")
            else:
                print("Неверный формат, повторите.")
            return

        number, code = int(parts[0]), parts[1]
        if code in self.seen_codes:
            if lineno:
                print(f"[Строка {lineno}] Пропущена: код '{code}' уже использован ранее.")
            else:
                print(f"Код '{code}' уже использован ранее, пропускаем.")
            return

        self.entries.append((number, code))
        self.seen_codes.add(code)

    def _sort_entries(self):
        """Сортирует входные данные по длине кода (от коротких к длинным)"""
        for i in range(1, len(self.entries)):
            key = self.entries[i]
            j = i - 1
            while j >= 0 and len(self.entries[j][1]) > len(key[1]):
                self.entries[j + 1] = self.entries[j]
                j -= 1
            self.entries[j + 1] = key
        return self.entries

def main():
    """Основная функция программы"""
    print("=== Построение двоичного дерева по кодам путей ===")

    while True:
        # Выбор режима ввода
        while True:
            mode = input("1 — из файла, 2 — вручную: ").strip()
            if mode in ('1', '2'):
                break
            print("Ошибка: введите 1 или 2")

        manager = TreeManager()
        input_handler = InputHandler()

        # Обработка выбранного режима
        if mode == '1':
            filename = input("Введите имя файла: ").strip()
            entries = input_handler.process_file(filename)
            if entries is None:  # Если файл не найден, начинаем сначала
                continue
        else:
            entries = input_handler.process_manual_input()

        # Построение дерева
        for number, code in entries:
            node = manager.ensure_path(manager.root, code,
                                     prompt_intermediate=True,
                                     prompt_final=False,
                                     final_value=number)
            if node.data != number:
                print(f"[Код '{code}'] узел уже = {node.data}, пропуск {number}.")

        # Вывод результатов
        manager.print_all()
        break  # Выход из основного цикла после успешного выполнения


if __name__ == "__main__":
    main()
