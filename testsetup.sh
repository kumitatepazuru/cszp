python3 setup.py sdist
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m pip install -i https://test.pypi.org/simple/ cuitools

