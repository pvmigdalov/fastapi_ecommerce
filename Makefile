.PHONY: app-up
app-up:
	docker compose up app -d

.PHONY: pg-up
pg-up:
	docker compose up pg -d

.PHONY: all-up
all-up:
	docker compose up -d

.PHONY: app-rebuild
app-rebuild:
	docker compose up app --build -d

.PHONY: pg-rebuild
pg-rebuild:
	docker compose up pg --build -d

.PHONY: all-rebuild
all-rebuild:
	docker compose up --build -d

.PHONY: all-stop
all-stop:
	docker compose stop

.PHONY: app-shell
app-shell:
	docker compose exec -it app bash

.PHONY: app-logs
app-logs:
	docker compose logs -f app

.PHONY: create-revision
create-revision:
	@if [ -z "$(MSG)" ]; then \
		echo "Error: MIGRATION name is required"; \
		echo "Usage: make migrate MIGRATION=\"Some description\""; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$(MSG)"

.PHONY: upgrade-head
upgrade-head: create-revision
	alembic upgrade head

.PHONY: migrate
migrate: upgrade-head
