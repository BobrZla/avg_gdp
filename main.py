# Здесь основной код скрипта
import argparse
import csv
import sys
from collections import defaultdict
from tabulate import tabulate

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

REQUIRED_HEADERS = [
    "country",
    "year",
    "gdp",
    "gdp_growth",
    "inflation",
    "unemployment",
    "population",
    "continent",
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


def _generate_average_gdp_report(all_data: list):
    """
    Генерирует и выводит отчет о среднем ВВП по странам.
    """
    country_gdp_values = defaultdict(list)

    for entry in all_data:
        country = entry.get("country")
        gdp = entry.get("gdp")  # Тут уже Float.

        if country and gdp is not None:
            country_gdp_values[country].append(gdp)

    average_gdps = []
    for country, gdps in country_gdp_values.items():
        if gdps:  # Исключаем деление на ноль.
            avg_gdp = sum(gdps) / len(gdps)
            average_gdps.append({"country": country, "gdp": round(avg_gdp, 2)})

    sorted_report_data = sorted(
        average_gdps, key=lambda x: x["gdp"], reverse=True
    )
    headers = {"country": "country", "gdp": "gdp"}
    print(
        tabulate(
            sorted_report_data,
            headers=headers,
            tablefmt="psql",
            numalign="right",
            showindex=range(1, len(sorted_report_data) + 1),
            floatfmt=".2f",
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="Анализ макроэкономичесских данных и создание отчетов."
    )
    # Аргумент --files: должен принимать одно или несколько значений (путей к файлам)
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
                reader = csv.DictReader(f)
                actual_headers = reader.fieldnames
                expected_headers_set = set(REQUIRED_HEADERS)
                actual_headers_set = set(actual_headers)
                if expected_headers_set != actual_headers_set:
                    print(
                        f"Ошибка: Шапка файла {file_path} "
                        f"Отличается от ожидаемой. "
                        f"Ожидаем: {expected_headers_set}, "
                        f"Получили: {actual_headers_set}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                for row in reader:
                    all_data.append(_process_row_types(row))
        except FileNotFoundError:
            print(
                f"Ошибка: Файл не найден по пути - {file_path}",
                file=sys.stderr,
            )
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка чтения файла {file_path}: {e}", file=sys.stderr)
            sys.exit(1)

    # Считаем ВВП.
    if args.report == "average-gdp":
        _generate_average_gdp_report(all_data)

    elif args.report:
        print(
            f'Ошибка: Неизвестный тип report "{args.report}".', file=sys.stderr
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
