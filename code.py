import os
import shutil


def replace_in_content(file_path, old_str, new_str):
    """Заменяет строку в содержимом файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = content.replace(old_str, new_str)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except (UnicodeDecodeError, PermissionError):
        pass  # Пропускаем бинарные файлы и файлы без прав доступа


def replace_in_name(path, old_str, new_str):
    """Заменяет строку в названии файла или папки и возвращает новый путь"""
    base_name = os.path.basename(path)
    dir_name = os.path.dirname(path)
    
    if old_str in base_name:
        new_name = base_name.replace(old_str, new_str)
        new_path = os.path.join(dir_name, new_name)
        os.rename(path, new_path)
        return new_path
    return path


def process_directory(root_dir, old_str, new_str):
    """Рекурсивно обрабатывает директорию"""
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        
        # Удаляем ненужные папки
        if item in ['.vs', 'build'] and os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Удалена папка: {item_path}")
            continue
        
        # Обрабатываем папки
        if os.path.isdir(item_path):
            new_item_path = replace_in_name(item_path, old_str, new_str)
            process_directory(new_item_path, old_str, new_str)
        
        # Обрабатываем файлы
        elif os.path.isfile(item_path):
            new_item_path = replace_in_name(item_path, old_str, new_str)
            replace_in_content(new_item_path, old_str, new_str)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 4:
        print("Использование: python script.py <путь_к_папке> <старая_строка> <новая_строка>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    old_string = sys.argv[2]
    new_string = sys.argv[3]
    
    if not os.path.isdir(folder_path):
        print(f"Ошибка: {folder_path} не является папкой или не существует")
        sys.exit(1)
    
    print(f"Обработка папки: {folder_path}")
    print(f"Замена '{old_string}' на '{new_string}'")
    
    process_directory(folder_path, old_string, new_string)
    
    print("Обработка завершена!")