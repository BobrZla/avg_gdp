import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
import pytest
from main import (
    _process_row_types,
    main,
    NUMERIC_FIELDS,
    _generate_average_gdp_report,
)
from unittest.mock import patch, mock_open


def test_process_row_types_converts_to_float():
    # Тестовая строка (словарь) с валидными данными.
    row = {
        "country": "TestCountry",
        "year": "2023",
        "gdp": "1234.56",
        "gdp_growth": "2.1",
        "inflation": "3.4",
        "unemployment": "3.7",
        "population": "100",
        "continent": "Europe",
    }

    processed_row = _process_row_types(row)

    assert processed_row["country"] == "TestCountry"
    assert processed_row["year"] == "2023"  # Возможно надо переводить в int
    assert isinstance(processed_row["gdp"], float)
    assert processed_row["gdp"] == 1234.56
    assert isinstance(processed_row["gdp_growth"], float)
    assert processed_row["gdp_growth"] == 2.1
    assert isinstance(processed_row["inflation"], float)
    assert processed_row["inflation"] == 3.4
    assert isinstance(processed_row["unemployment"], float)
    assert processed_row["unemployment"] == 3.7
    assert isinstance(processed_row["population"], float)
    assert processed_row["population"] == 100.0
    assert processed_row["continent"] == "Europe"


def test_process_row_types_handles_non_numeric_values(capsys):
    # Тестовая строка с неверными числовыми значениями.
    row = {
        "country": "Название страны",
        "gdp": "Попытка передать не число",
        "gdp_growth": "",  # Пустая строка.
        "inflation": "5.0",
    }
    processed_row = _process_row_types(row)
    captured = capsys.readouterr()

    assert (
        'ОШИБКА: Не удалось конвертировать "Попытка передать не число"'
        in captured.err
    )
    assert processed_row["country"] == "Название страны"
    assert processed_row["gdp"] == 0.0
    assert processed_row["gdp_growth"] == 0.0
    assert processed_row["inflation"] == 5.0


def test_process_row_types_handlers_missing_fields():
    # Тут мы убираем некоторые числовые значения и исходной строке (словаре).
    row = {"country": "reviewer is cool", "gdp": "100.0"}
    processed_row = _process_row_types(row)

    assert processed_row["country"] == "reviewer is cool"
    assert processed_row["gdp"] == 100.0
    # Поля которых нету станут нулями (сообщение об ошибке пользователю).
    for field in [f for f in NUMERIC_FIELDS if f not in row]:
        assert processed_row[field] == 0.0


def test_main_with_valid_arguments_calls_report_generator(capsys):
    """
    Проверяем, что main() успешно парсит аргументы
    и вызывает функцию для генерации отчета.
    """
    test_args = [
        "main.py",
        "--files",
        "test_data.csv",
        "--report",
        "average-gdp",
    ]

    mock_csv_content = """country,year,gdp,gdp_growth,inflation,unemployment,population,continent
    TestCountry,2023,100.00,1.0,1.0,1,NA
    """

    with patch.object(sys, "argv", test_args):
        with patch(
            "builtins.open", mock_open(read_data=mock_csv_content)
        ) as m_open:
            with patch(
                "main._generate_average_gdp_report"
            ) as mock_generate_report:
                main()

                m_open.assert_called_with(
                    "test_data.csv", mode="r", encoding="utf-8"
                )
                mock_generate_report.assert_called_once()

    captured = capsys.readouterr()
    assert "Error" not in captured.err
    assert "Warning" not in captured.err
    assert "Ошибка" not in captured.err


def test_main_missing_files_argument_exits_with_error(capsys):
    """
    Проверяет, что main() завершится с ошибкой, если отсутствует --files.
    """
    test_args = ["main.py", "--report", "average-gdp"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()
        captured = capsys.readouterr()

        assert (
            "the following arguments are required: --files" in captured.err
            or "Следующие аргументы являются обязательными: --files"
            in captured.err
        )
        assert excinfo.value.code != 0


def test_main_missing_report_argument_exits_with_error(capsys):
    """
    Проверяет, что main() завершится с ошибкой, если отсутствует --report.
    """
    test_args = ["main.py", "--files", "average-gdp"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()
        captured = capsys.readouterr()

        assert (
            "the following arguments are required: --report" in captured.err
            or "Следующие аргументы являются обязательными: --report"
            in captured.err
        )
        assert excinfo.value.code != 0


def test_main_unknown_report_type_exits_with_errors(capsys):
    """
    Проверяет, что main() завершится с ошибкой если тип отчета неизвестен.
    """
    test_args = [
        "main.py",
        "--files",
        "test_data.csv",
        "--report",
        "Неизвестное-название-report",
    ]
    mock_csv_content = """country,year,gdp,gdp_growth,inflation,unemployment,population,continent
    TestCountry,2023,100.00,1.0,1.0,1,NA
    """
    with patch.object(sys, "argv", test_args):
        with patch("builtins.open", mock_open(read_data=mock_csv_content)):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code != 0
            captured = capsys.readouterr()
            assert "Ошибка: Неизвестный тип report" in captured.err


def test_main_non_existent_file_exits_with_errors(capsys):
    """
    Проверяет, что main() завершается с ошибкой
    при попытке открыть несуществующий файл.
    """
    test_args = [
        "main.py",
        "--files",
        "Несуществующий_файл.csv",
        "--report",
        "average-gdp",
    ]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code != 0
        captured = capsys.readouterr()
        assert "Ошибка: Файл не найден по пути" in captured.err


def test_main_file_read_error_exits_with_error(capsys):
    """
    Проверяет, что main() завершается с ошибкой при возникновении
    непредвиденной ошибки чтения файла.
    Например: файл где-то уже открыт, или нет прав доступа или файл битый.
    """
    test_args = [
        "main.py",
        "--files",
        "Битый_файл.csv",
        "--report",
        "average-gdp",
    ]
    with patch.object(sys, "argv", test_args):
        with patch(
            "builtins.open", side_effect=OSError("Simulated read error")
        ):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code != 0
            captured = capsys.readouterr()
            assert "Ошибка чтения файла" in captured.err


def test_main_missing_required_headers_exits_with_error(capsys):
    """
    Проверяет что будет ошибка если в csv файле нет всех заголовков (headers).
    """
    test_args = [
        "main.py",
        "--files",
        "Файл_без_всех_заголовков.csv",
        "--report",
        "average-gdp",
    ]
    # Тут не хватает заголовка 'gdp'.
    mock_csv_content = """country,year,gdp_growth,inflation,unemployment,population,continent
    TestCountry,2023,100.00,1.0,1.0,1,NA
    """
    with patch.object(sys, "argv", test_args):
        with patch("builtins.open", mock_open(read_data=mock_csv_content)):
            with pytest.raises(SystemExit) as excinfo:
                main()

            assert excinfo.value.code != 0
            captured = capsys.readouterr()
            assert "Ошибка: Шапка файла" in captured.err


def test_generate_average_gdp_report_calculates_and_sorts_correctly(capsys):
    """
    Проверяет, что _generate_average_gdp_report правильно считает среднее ВВП
    и сортирует данные.
    """
    sample_data = [
        {
            "country": "CountryA",
            "year": "2021",
            "gdp": 100.0,
            "gdp_growth": 0.0,
            "inflation": 0.0,
            "unemployment": 0.0,
            "population": 0.0,
            "continent": "X",
        },
        {
            "country": "CountryA",
            "year": "2022",
            "gdp": 200.0,
            "gdp_growth": 0.0,
            "inflation": 0.0,
            "unemployment": 0.0,
            "population": 0.0,
            "continent": "X",
        },
        {
            "country": "CountryB",
            "year": "2021",
            "gdp": 500.0,
            "gdp_growth": 0.0,
            "inflation": 0.0,
            "unemployment": 0.0,
            "population": 0.0,
            "continent": "Y",
        },
        {
            "country": "CountryB",
            "year": "2022",
            "gdp": 100.0,
            "gdp_growth": 0.0,
            "inflation": 0.0,
            "unemployment": 0.0,
            "population": 0.0,
            "continent": "Y",
        },
        {
            "country": "CountryC",
            "year": "2021",
            "gdp": 400.0,
            "gdp_growth": 0.0,
            "inflation": 0.0,
            "unemployment": 0.0,
            "population": 0.0,
            "continent": "Z",
        },
    ]
    expected_output_lines = [
        "+----+-----------+--------+",
        "|    | country   |    gdp |",
        "|----+-----------+--------|",
        "|  1 | CountryC  | 400.00 |",
        "|  2 | CountryB  | 300.00 |",
        "|  3 | CountryA  | 150.00 |",
        "+----+-----------+--------+",
    ]
    _generate_average_gdp_report(sample_data)
    captured = capsys.readouterr()
    actual_output_lines = [line.strip() for line in captured.out.splitlines()]

    assert actual_output_lines == expected_output_lines
    assert captured.err == ""


def test_generate_average_gdp_report_with_empty_data(capsys):
    """
    Проверяет, что _generate_average_gdp_report
    корректно обрабатывает пустые данные.
    """
    empty_data = []
    _generate_average_gdp_report(empty_data)
    captured = capsys.readouterr()
    expected_output_lines = [
        "+-----------+-------+",
        "| country   | gdp   |",
        "|-----------+-------|",
        "+-----------+-------+",
    ]
    actual_output_lines = [line.strip() for line in captured.out.splitlines()]

    assert actual_output_lines == expected_output_lines
    assert captured.err == ""
