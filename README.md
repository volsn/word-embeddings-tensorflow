# Классификатор статей
Реализован с помошью таких технологий как python, scrapy, flask, keras

## Парсинг
Осуществляется за счет фреймворка scrapy.

#### Вызов парсинга
```bash
scrapy crawl rss -a input=input.txt -o output.json
```

#### Пример txt
```txt
https://www.buzzfeed.com/health.xml
https://www.buzzfeed.com/tech.xml
...
```

## Обучение модели
Использован фреймворм Keras, а также векторное представление слов GloVe
необходимые файлы:
* dataset_full.txt - полный датасет в формате csv, хранящий дополнительные параметры
* dataset_short.txt - сокоращенный датасет в формате csv, хранящий параметры необходимые для обучения модели
* tokenizer.pickle - генератор меток для текста
* embeddings.pickle - векторное представление слов, оптимизированное для используемого генератора меток
* classifier.hdf5 - классификатор, сохраненный в формате HDF5
* FitModel.py - скрипт для обучения модели

## Развертывание приожения
Запуск просиходит при помощи следующих комманд
```bash
Linux/MacOS:
export FLASK_APP=app.py
flask run

Windows:
python app.py
```

Реализована возможность развертывания системы в Docker.
