# Здесь основной код скрипта
import argparse
import csv
import sys

"""
Константа для модуля преобразования,
Тут указаны поля которые должны быть числами Float.
"""
NUMERIC_FIELDS = [
    "gdp",
    "gdp_growth",
    "inflation",
    "unemployment",
    "population",
]


def _process_row_types(row: dict) -> dict:
    """
    Получает словарь где меняет тип поля из NUMERIC_FIELDS из str в float.
    """
    processed_row = row.copy()
    for field in NUMERIC_FIELDS:
        if field in processed_row and processed_row[field]:
            try:
                processed_row[field] = float(processed_row[field])
            except ValueError:
                print(
                    f"ОШИБКА: Не удалось конвертировать "
                    f'"{processed_row[field]}" в число в поле "{field}". '
                    f"Ставим значени по умолчанию 0.0",
                    file=sys.stderr,
                )
                processed_row[field] = 0.0
        else:
            # Если поле отсутствует или пустое, ставим значение по умолчанию.
            processed_row[field] = 0.0
    return processed_row


def main():
    parser = argparse.ArgumentParser(
        description="Анализ макроэкономичесских данных и создание отчетов."
    )
    # Аргумент --files: должен принимать одно или несколько значений (путей к файлам)
    # nargs='+' означает "один или более" аргументов
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к одному или нескольким CSV-файлам, содержащим экономические данные.",
    )

    # Аргумент --report: принимает одно строковое значение (название отчета)
    parser.add_argument(
        "--report",
        type=str,
        required=True,
        help='Название отчета для создания (например: "average-gdp").',
    )
    args = parser.parse_args()
    all_data = []  # Тут будем хранить данные из csv файлов.

    for file_path in args.files:
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                # csv.DictReader позволяет читать строки как словари, где ключи - это заголовки
                reader = csv.DictReader(f)
                for row in reader:
                    # Каждая строка - это словарь {'country': 'USA', 'year': 1992}
                    all_data.append(_process_row_types(row))
        except FileNotFoundError:
            print(
                f"Ошибка: Файл не найден по пути - {file_path}",
                file=sys.stderr,
            )
            sys.exit(1)
        except Exception as e:
            print("Ошибка чтения файла {file_path}: {e}", file=sys.stderr)
            sys.exit(1)

    print(
        f"Успешно загруженны {len(all_data)} данных из {len(args.files)} файлов."
    )

    if all_data:
        print("первый ввод данных после преобразования типов:", all_data[0])
        print(f'Тип "gdp" в первом прогоне: {type(all_data[0].get("gdp"))}')
    # Тестовый принт
    print(f"Файлы для обработки: {args.files}")
    print(f"Отчеты для создания: {args.report}")

    # Дописать остальной код для обработки


if __name__ == "__main__":
    main()
