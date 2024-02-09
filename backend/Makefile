# start docker container
MYSQL_CONTAINER_NAME = Qinfo-mysql

start:
	sudo docker start $(MYSQL_CONTAINER_NAME)
	flask run

stop:
	docker stop $(MYSQL_CONTAINER_NAME)
