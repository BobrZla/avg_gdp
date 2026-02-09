# Здесь основной код скрипта
import argparse
import csv
import sys


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
    all_data = [] # Тут будем хранить данные из csv файлов.

    for file_path in args.files:
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                # csv.DictReader позволяет читать строки как словари, где ключи - это заголовки
                reader = csv.DictReader(f)
                for row in reader:
                    # Каждая строка - это словарь {'country': 'USA', 'year': 1992}
                    all_data.append(row)
        except FileNotFoundError:
            print(f'Ошибка: Файл не найден по пути - {file_path}', file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print('Ошибка чтения файла {file_path}: {e}', file=sys.stderr)
            sys.exit(1)

    print(f'Успешно загруженны {len(all_data)} данных из {len(args.files)} файлов.')

    if all_data:
        print("Первая запись:", all_data[0])

    # Тестовый принт
    print(f"Файлы для обработки: {args.files}")
    print(f"Отчеты для создания: {args.report}")

    # Дописать остальной код для обработки


if __name__ == "__main__":
    main()
