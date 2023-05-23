# Makefile

# Define targets and their dependencies
up:
	docker-compose up

down:
	docker-compose down --rmi all
