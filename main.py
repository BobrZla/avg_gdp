# Здесь основной код скрипта
import argparse
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

    # Тестовый принт
    print(f"Файлы для обработки: {args.files}")
    print(f"Отчеты для создания: {args.report}")

    # Дописать остальной код для обработки


if __name__ == "__main__":
    main()
