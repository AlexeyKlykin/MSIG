help:
	@echo "start_db - start postgres"
	@echo "exec -  -it postgres psql -h localhost -U neon185a -d msig"
	@echo "build - build -t postgresql:latest . "
	@echo "clean - stop postgres && docker rm postgres"
	@echo "run - run --name postgres -e POSTGRES_PASSWORD=vbnzq185a -e POSTGRES_USER=neon185a -e POSTGRES_DB=msig -p 5432:5432 -d postgresql:latest"
	@echo "create_db"
start_db:
	@docker start postgres
# exec:
# 	@docker exec -ti msig_postgres psql -h localhost -U postgres
exec:
	@docker exec -it msig_postgres psql -h localhost -U neon185a -d msig
build:
	@docker build -t msig_postgres:latest .
# run:
# 	@docker run --name msig_postgres -e POSTGRES_PASSWORD=vbnzq185a -p 5432:5432 -d msig_postgres:latest
run:
	@docker run --name msig_postgres -e POSTGRES_PASSWORD=vbnzq185axe -e POSTGRES_USER=neon185a -e POSTGRES_DB=msig -p 5432:5432 -d msig_postgres:latest
clean:
	@docker stop msig_postgres && docker rm msig_postgres
stop:
	docker stop msig_postgres
