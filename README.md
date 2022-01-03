# halfplane

# Usage

```
pip install halfplane
```

## Plot examples

```
python -m hyperplane.plots
```

The results are dumped to `./plots/`.

## Test

```
pytest
```

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
