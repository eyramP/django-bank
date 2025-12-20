build:
	docker compose -f local.yml up --build -d --remove-orphans

down:
	docker compose -f local.yml down 
logs_api:
	docker compose -f local.yml logs api

logs_mailpit:
	docker compose -f local.yml logs mailpit

logs_postgres:
	docker compose -f local.yml logs postgres

inspect_nw:
	docker network inspect banker_local_nw