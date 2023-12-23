sudo docker compose down
sudo docker compose up --build -d
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic --no-input
sudo docker compose exec backend cp -r /backend/collected_static/. /backend_static/static/ 