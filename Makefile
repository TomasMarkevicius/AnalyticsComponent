run:
	python3 __main__.py

run_tests:
	python3 -m unittest discover tests

install_reqs:
	python3 -m pip install -r requirements.txt

run_docker:
	docker-compose up analytics