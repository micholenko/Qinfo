# start docker container
MYSQL_CONTAINER_NAME = Qinfo-mysql

start:
	python run.py

start-db:
	sudo docker start $(MYSQL_CONTAINER_NAME)

fill-db:
	python fill_db.py

test:
	pytest -v -s

stop:
	docker stop $(MYSQL_CONTAINER_NAME)
