# Проект парсинга документации PEP.

## Стек технологий:

**[argparse](https://docs.python.org/3/library/argparse.html),
 [logging](https://docs.python.org/3/library/logging.html),
 [regular expression](https://docs.python.org/3.9/library/re.html),
 [requests_cache](https://requests-cache.readthedocs.io/en/stable/),
 [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/),
 [prettytable](https://ptable.readthedocs.io/en/latest/tutorial.html)**

## Описание:

Данный проект написан в учебных целях и представлет собой простейший парсер документации питоно, в частности
 [списка PEP](https://peps.python.org/), а так же способен выкачивать самую новую документацию по
 [python 3](https://docs.python.org/3/).

Модуль [```argparse```](https://docs.python.org/3/library/argparse.html) позволяет эффективно разобрать параметры
передваемые в командной строке и выбрать соответствующую стратегию поведения.

реультат выполнения команды: ```python main.py -h```

> main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}
>
> Парсер документации Python
>
> positional arguments:
>   {whats-new,latest-versions,download,pep}
>                         Режимы работы парсера
>
> options:
>   -h, --help            show this help message and exit
>   -c, --clear-cache     Очистка кеша
>   -o {pretty,file}, --output {pretty,file}
>                         Дополнительные способы вывода данных

По команде ```whats-new``` можно посмотреть ссылки на дайджесты о нововведениях в различных версиях python.

```latest-version``` возвращает ссылки на все версии питона с их текущими статусами.

```pep``` статистику по всем имеющимся на текущи й момент PEP.

А команда ```download``` позволяет выкачать архив с последней документацией python.

За процесс парсинга отвечает библиотека [```BeautifulSoup```](https://beautiful-soup-4.readthedocs.io/en/latest/).
 Именно с её помощью происходит выбор нужных данных. Вывод статусбара базируется на библиотеке
 [```tqdm```](https://tqdm.github.io/), а вывод табличных значений в красивом виде происходит за счёт
 [```prettytable```](https://ptable.readthedocs.io/en/latest/tutorial.html).

В целях экономии трафика и для проведения процесса тестирования и отладки было организовано кэширование запросов к
 внешним ресурсам с помощью библиотеки [```requests_cache```](https://requests-cache.readthedocs.io/en/stable/). При
 необходимости кэш можно очистить.

## Запуск

Если вы собираетесь работать из командной строки в **windows**, вам может
 потребоваться Bash. скачать его можно по ссылке:
 [GitBash](https://gitforwindows.org/) ([Git-2.33.0.2-64-bit.exe](https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0.2-64-bit.exe)).

Так же при работе в **windows** необходимо использовать **python** вместо
 **python3**

Последнюю версию **python** ищите на официальном сайте
 [https://www.python.org/](https://www.python.org/downloads/)

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/zhss1983/bs4_parser_pep
```

```
cd bs4_parser_pep
```

Создать и активировать виртуальное окружение:

```
python -m venv env
```

- linux
```
source env/bin/activate
```
- windows
```
source env/Scripts/activate
```

Установить зависимости из файла **requirements.txt**:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить рограмму:

```
python src/main.py -h
```
