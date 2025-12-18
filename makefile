local-run:
	python manage.py init_project
	python manage.py runserver

mig:
	python manage.py makemigrations
	python manage.py migrate
