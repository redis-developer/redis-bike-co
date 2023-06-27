# Jupyter Notebook w/ Rise Presentation

## Add the requirement using `poetry add`

```
poetry add -D jupyter
poetry add RISE
poetry add hide_code
poetry add plotly

poetry run jupyter nbextension install --py --user hide_code
poetry run jupyter nbextension enable --py --user hide_code
poetry run jupyter serverextension enable --py --user hide_code
```

## Launch the Notebook

```
poetry run jupyter notebook
``