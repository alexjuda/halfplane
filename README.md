# halfplane

# Usage

```
pip install halfplane
```

TBD

# Dev set up

```
pyenv virtualenv $(basename $PWD)
pyenv local $(basename $PWD)
pip install --upgrade pip
pip install -e .[dev]
```

# Release

```
pip install build twine
python -m build
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```
