# Поиск лучшей вакансии
При помощи этого проекта вы можете посмотреть статистику самых оплачиваемых языков программирования в двух сайтах: HeadHunter и SuperJob.

### Как установить

На компьютере пользователя должен быть установлен Python3.
Затем используйте `pip` (или `pip3`, есть конфликт Python2) для установки зависимостей:
```
pip install -r requirments.txt
``` 
Рекомендуется использовать [virtulenv/venv](https://docs.pythpn.org/3/library/venv.html) для изоляци проекта.

### Переменные окружения

В этом проекте используется одна переменная окружения: SuperJob_API. Чтобы она появилась в проекте, Вам необходимо создать файл .env, а после в нем написать следующую строку:
```
SuperJob_API=Ваш ключ,
```
где вместо Ваш ключ надо подставить свой секретный ключ от сайта SuperJob.

### Как работает

Чтобы запустить проект, Вам необходимо перейти в командной строке в папку, где находится проект и написать:
```
python TerminalTable.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).