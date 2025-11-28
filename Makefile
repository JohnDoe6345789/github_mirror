
install:
	pip install -r requirements.txt
test:
	pytest -q
type:
	mypy mirror.py
