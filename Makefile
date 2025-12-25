build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

config:
	docker compose -f local.yml config

logs_api:
	docker compose -f local.yml logs api

logs_mailpit:
	docker compose -f local.yml logs mailpit

logs_postgres:
	docker compose -f local.yml logs postgres

logs_nginx:
	docker compose -f local.yml logs nginx

logs_rabbitmq:
	docker compose -f local.yml logs rabbitmq

inspect_nw:
	docker network inspect banker_local_nw

migrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic --no-input --clear

su:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

flush:
	docker compose -f local.yml run --rm api python manage.py flush

connect_db:
	docker compose -f local.yml exec postgres psql --username=eyram --dbname=banker

down-v:
	docker compose -f local.yml down -v