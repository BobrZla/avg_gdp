📊 Анализатор макроэкономических данных
Проект для анализа CSV-файлов с макроэкономическими показателями стран и формирования отчетов.

## Установка
```bash
# Клонируйте репозиторий
git clone https://github.com/BobrZla/avg_gdp.git
cd avg_gdp

# Создайте виртуальное окружение (опционально)
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate     # для Windows

# Установите зависимости
pip install -r requirements.txt
```
## Запуск
Для удобства создайте в корне папку <span style="color: green"> "data" </span> и поместите туда ваши .csv файлы, например названиея будут <span style="color: green"> economic1.csv </span> и <span style="color: green"> economic2.csv </span> .
```bash
# Базовый запуск
python main.py --files data/economic1.csv --report average-gdp

# С несколькими файлами
python main.py --files data/economic1.csv data/economic2.csv --report average-gdp
```
## Пример вывода.
```bash
+----+----------------+----------+
|    | country        |      gdp |
|----+----------------+----------|
|  1 | United States  | 23923.67 |
|  2 | China          | 17810.33 |
|  3 | Japan          |  4467.00 |
|  4 | Germany        |  4138.33 |
|  5 | India          |  3423.67 |
|  6 | United Kingdom |  3113.33 |
|  7 | France         |  2834.67 |
|  8 | Canada         |  2096.33 |
|  9 | Russia         |  2077.67 |
| 10 | Italy          |  2042.00 |
| 11 | Brazil         |  1900.67 |
| 12 | South Korea    |  1727.33 |
| 13 | Australia      |  1637.00 |
| 14 | Spain          |  1409.33 |
| 15 | Mexico         |  1392.67 |
| 16 | Indonesia      |  1274.33 |
| 17 | Saudi Arabia   |  1016.33 |
| 18 | Netherlands    |  1006.00 |
| 19 | Turkey         |   927.33 |
| 20 | Switzerland    |   845.00 |
+----+----------------+----------+
```
## Требования
- Python 3.10

- Зависимости указаны в requirements.txt

# Для ревьюера.
![Pytest](./screenshots/pytest.png)
