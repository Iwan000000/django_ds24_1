Развертывание приложения
Перед развертыванием приложения убедитесь, что у вас установлены следующие компоненты:

    Docker

    Docker Compose

Шаг 1: Клонирование репозитория
Сначала необходимо клонировать репозиторий с приложением на ваш локальный компьютер. Это можно сделать с помощью команды:

    git clone https://github.com/Iwan000000/django_ds24_1.git


Шаг 2: Настройка переменных окружения
Создайте файл (.env) в корневой директории проекта и заполните его переменными окружения:


    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=
    SUPER_USER=
    SUPER_USER_PASS=
    STRIPE_API_KEY=
    SECRET_KEY=
    REDIS_URL=
    MAIL_USER=
    MAIL_PASS=

Шаг 3: Запуск Docker-контейнеров
Перейдите в корневую директорию проекта и запустите Docker-контейнеры с помощью Docker Compose:


    cd /path/to/your/project
    docker-compose up -d

Опция -d позволяет запустить контейнеры в фоновом режиме.

Шаг 4: Применение миграций
После запуска контейнеров приложению необходимо применить миграции базы данных. Для этого выполните следующую команду внутри контейнера Django:


    docker-compose exec app python manage.py migrate

Шаг 5: Запуск приложения
Теперь приложение должно быть готово к использованию. Вы можете открыть браузер и перейти по адресу http://localhost:8000, чтобы увидеть приложение.

Шаг 6: Остановка и удаление контейнеров
Чтобы остановить и удалить контейнеры, выполните следующую команду в корневой директории проекта:


    docker-compose down

Эта команда остановит и удалит все контейнеры, сети и тома, которые были созданы при запуске Docker Compose.
