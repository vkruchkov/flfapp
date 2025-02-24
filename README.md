# flfapp
## Описание
Программа First Latvian Fusker' Ripper предназначена для автоматизированного сохранения изображений с сайта <https://www.fusker.xxx>.<BR>
HTML код на указанном сайте формируется динамически при помощи JS, поэтому для чтения страниц сайта программа использует библиотеку Selenium WebDriver (<https://www.selenium.dev/>) для запуска браузера FireFox в режиме headless.<BR>
Программа с периодичностью в 60 секунд обращается к основной странице сайта, отслеживая появление новых публикаций.<BR>
С основной страницы сайта считывается список всех последних публикаций. Публикация однозначно идентифицируется по ID (e.g. `https://www.fusker.xxx/en/?lid=3795970`). ID обработанных публикаций сохраняются в локальной БД. Если при обработке основной страницы сайта обнаружена публикация с ID, отсутствующей в БД, то такая публикация считается новой. Обработка вновь обнаруженных публикаций происходит параллельно в несколько потоков. Максимальное количество параллельнных потоков определяется настройками.<BR>
Каждая публикация содержит одно или несколько изображений из одного определенного источника (e.g. thehentai.net, ilikecomix.com etc).
Не все источники одинаково полезны, поэтому реализован механизм "черного списка". "Черный список" представляет собой текстовый файл с набором регулярных выражений. При обработке очередной публикации, весь набор регулярных выражений по одному в цикле применяется к строке источника. При положительном результате, дальнейшая обработка данной публикации не производится, изображения не сохраняются. Готовый пример "черного списка" прилагается. "Черный список" перечитывается программой автоматически после редактирования файла, что позволяет обновлять "черный список" без перезапуска програмы.<BR>
Если источник вновь обнаруженной публикации не попадает в "черный список", то программа создает директорию для данной публикации, и сохраняет в неё все изображения, обнаруженные в публикации. Для каждого изображения вычисляется сумма длины и ширины этого изображения, и сравнивается с заданным порогом в настройках. Если ни одно изображение в публикации не превышает установленного порога, то все сохраненные изображения для данной публикации удаляются вместе с директорией.<BR>
Для сохранения изображений используется следующая структура директорий:<BR>
корневая директория, определенная в настройках (e.g. files/)<BR>
~~ директория источника (e.g. thehentai.net/)<BR>
~~~~ директория публикации (e.g. 3795970/)<BR>

## Установка
- Скопировать файлы *.py, FirstLatvianFusker.cfg, black.list в отдельную директорию
- Создать виртуальное окружение:<BR>
`python -m venv venv`<BR>
`source venv/bin/activate`
- Установить необходимые библиотеки:<BR>
`pip install Pillow`<BR>
`pip install selenium`
- Внести необходимые изменения в файл конфигурации
- Запустить программу, набрав в терминале `./venv/bin/python main.py` или просто `flfapp.sh`<BR>
Завершить выполнение программы можно комбинацией клавишей Ctrl-C.<BR> 
Логи программы удобно мониторить командой `tail -f FirstLatvianFusker.log` , запущенной в отдельном окне терминала.

## Конфигурация
Описание параметров файла конфигурации
- url (str): URL основной страницы сайта. По умолчанию: 'https://www.fusker.xxx/en/'
- logname (str): Путь и имя файла лога. По умолчанию: `FirstLatvianFusker.log`
- loglevel (str): Уровень логирования [DEBUG, INFO, WARNING, ERROR, CRITICAL]. По умолчанию: INFO
- basepath (str): Путь к базовой директории для сохранения изображений. По умолчанию: поддиректория `files` от директории установки.
- pageurl (str): Суффикс URL, который определяет путь к конкретной публикации. По умолчанию: `?lid=`
- database (str): Полный путь и имя файла БД. По умолчанию: `flf.db`
- max_threads (int): Максимальное количество параллельных потоков для обработки публикаций. По умолчанию: 10
- blacklist (str): Полный путь и имя файла "черного списка". По умолчанию: `black.list`
- threshold (int/float): Пороговое значение для суммы длины и ширины изображения. По умолчанию: 1500
- hold_days (int): Количество дней дня хранения ID публикаций в БД. По умолчанию: 3
- timeout (int): Таймаут для чтения web-страниц. По умолчанию: 15 секунд.
- geckodriver_path (str): Путь к драйверу Geckodriver для Selenium WebDriver. По умолчанию: `/usr/local/bin/geckodriver`

## Запуск в виде службы 
Опишу позднее, если нужно

## Требования
- Python 3.*
- установленный браузер FireFox
- Библиотеки Pillow и selenium
