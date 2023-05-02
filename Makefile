remove-volumes:
	docker-compose down --volumes

start:
	docker-compose up

stop:
	docker-compose down

restart-api:
	docker restart aiproductsystem-api-1

inspect-db-host:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' loanbot-postgres-1

docker-prune:
	docker image prune && docker volume prune && docker container prune
