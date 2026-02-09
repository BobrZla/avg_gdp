import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
import pytest
from main import _process_row_types, main, NUMERIC_FIELDS
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


def test_process_row_types_handles_non_numeric_values():
    # Тестовая строка с неверными числовыми значениями.
    row = {
        "country": "Название страны",
        "gdp": "Попытка передать не число",
        "gdp_growth": "",  # Пустая строка.
        "inflation": "5.0",
    }
    processed_row = _process_row_types(row)

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
