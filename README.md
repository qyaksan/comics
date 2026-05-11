Требования:

Установленный Docker Desktop (или Docker + docker-compose)

Git (для клонирования)

Шаги:

Клонируйте репозиторий:

bash
git clone https://github.com/ВАШ_ЛОГИН/comic-reader.git
cd comic-reader
Запустите контейнеры:

bash
docker compose up -d
Выполните миграции и создайте администратора:

bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
Откройте в браузере: http://localhost:8000
