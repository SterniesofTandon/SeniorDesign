PYLINT = flake8

FORCE:

dev_env: FORCE
	pip3 install -r requirements-dev.txt

tests: FORCE
	$(PYLINT) *.py
	nosetests hello.py --exe --with-coverage --verbose --cover-package=SeniorDesign

deploy:
	python ./venv/app/app.py

prod:
	- git commit -a
	- git pull
	- git push

%.py: FORCE
	nosetests tests.test_$* --nocapture
