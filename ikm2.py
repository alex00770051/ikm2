import re


class Node:
    """Класс узла бинарного дерева.

    Атрибуты:
        data (int): значение, хранящееся в узле
        left (Node): левый потомок
        right (Node): правый потомок
    """

    def __init__(self, data=None):
        """Инициализирует узел с заданным значением.

        Args:
            data (int, optional): значение узла. По умолчанию None.
        """
        self.data = data
        self.left = None
        self.right = None


class TreeManager:
    """Класс для управления построением дерева и взаимодействием с пользователем."""

    def __init__(self):
        """Инициализирует менеджер с пустым деревом (корневой узел со значением 0)."""
        self.root = Node(0)

    def ensure_path(self, node, code, prompt_intermediate, prompt_final, final_value=None):
        """Создает путь в дереве по заданному коду (рекурсивная реализация).

        Args:
            node (Node): текущий узел
            code (str): оставшаяся часть кода пути
            prompt_intermediate (bool): запрашивать ли значения для промежуточных узлов
            prompt_final (bool): запрашивать ли значение для конечного узла
            final_value (int, optional): значение для конечного узла

        Returns:
            Node: конечный узел в пути
        """
        if not code:
            if final_value is not None:
                node.data = final_value
            return node

        branch = 'left' if code[0] == '0' else 'right'
        child = getattr(node, branch)

        if child is None:
            if (len(code) > 1 and prompt_intermediate) or (len(code) == 1 and prompt_final):
                while True:
                    text = input(
                        f"Введите целое для {'промежуточного' if len(code) > 1 else 'конечного'} "
                        f"узла '{code[0]}' (от '{code}')': "
                    ).strip()
                    if text.isdigit():
                        child = Node(int(text))
                        break
                    print("Ошибка: нужно целое неотрицательное число.")
            else:
                child = Node()
            setattr(node, branch, child)

        return self.ensure_path(child, code[1:], prompt_intermediate, prompt_final, final_value)

    def collect_nodes(self, node, path="", out=None):
        """Рекурсивно собирает все узлы дерева в список.

        Args:
            node (Node): текущий узел
            path (str): текущий путь
            out (list): список для сбора результатов

        Returns:
            list: список кортежей (путь, значение)
        """
        if out is None:
            out = []
        out.append((path, node.data))
        if node.left:
            self.collect_nodes(node.left, path + "0", out)
        if node.right:
            self.collect_nodes(node.right, path + "1", out)
        return out

    def print_tree(self, node, level=0):
        """Рекурсивно печатает дерево в горизонтальном виде.

        Args:
            node (Node): текущий узел
            level (int): текущий уровень вложенности
        """
        if node.right:
            self.print_tree(node.right, level + 1)
        print("    " * level + f"-> {node.data}")
        if node.left:
            self.print_tree(node.left, level + 1)

    def insert_from_file(self, filename):
        """Строит дерево на основе данных из файла."""
        entries = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for lineno, line in enumerate(f, 1):
                    text = line.strip()
                    if not text:
                        continue
                    parts = text.split()
                    if len(parts) != 2 or not parts[0].isdigit() or any(ch not in '01' for ch in parts[1]):
                        print(f"[Строка {lineno}] Пропущена: ожидается '<число> <код>'.")
                        continue
                    entries.append((int(parts[0]), parts[1]))
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            exit(1)

        entries.sort(key=lambda x: len(x[1]))
        for number, code in entries:
            node = self.ensure_path(
                self.root,
                code,
                prompt_intermediate=True,
                prompt_final=False,
                final_value=number
            )
            if node.data != number:
                print(f"[Код '{code}'] узел уже = {node.data}, пропуск {number}.")

    def insert_manually(self):
        """Позволяет пользователю вручную вводить данные для дерева."""
        entries = []
        print("Ручной ввод. Формат: <число> <код 0/1>, 'q' — выход.")
        while True:
            s = input("> ").strip()
            if s.lower() == 'q':
                break
            parts = s.split()
            if len(parts) != 2 or not parts[0].isdigit() or any(ch not in '01' for ch in parts[1]):
                print("Неверный формат, повторите.")
                continue
            entries.append((int(parts[0]), parts[1]))

        entries.sort(key=lambda x: len(x[1]))
        for number, code in entries:
            node = self.ensure_path(
                self.root,
                code,
                prompt_intermediate=True,
                prompt_final=False,
                final_value=number
            )
            if node.data != number:
                print(f"[Код '{code}'] узел уже = {node.data}, пропуск {number}.")

    def print_all(self):
        """Выводит полную информацию о дереве."""
        print("\nСписок узлов (код путь : значение):")
        for path, val in self.collect_nodes(self.root):
            print(f"{path or 'root':>5} : {val}")

        print("\nГоризонтальное представление дерева:")
        self.print_tree(self.root)


def main():
    """Точка входа в программу."""
    print("=== Построение двоичного дерева по кодам путей ===")
    mode = input("1 — из файла, 2 — вручную: ").strip()
    manager = TreeManager()

    if mode == '1':
        filename = input("Введите имя файла: ").strip()
        manager.insert_from_file(filename)
    else:
        manager.insert_manually()

    manager.print_all()


if __name__ == "__main__":
    main()