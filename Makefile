.PHONY: app
app:
	docker compose up app --build -d

.PHONY: pg
pg:
	docker compose up pg --build -d

.PHONY: all-up
all-up:
	docker compose up --build -d

.PHONY: all-stop
all-stop:
	docker compose stop

.PHONY: app-shell
app-shell:
	docker compose exec -it app bash
