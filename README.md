# MSVDD + Bloc

(Microsoft + DataKind AI in Cities Virtual Accelerator - DataDive) + (Bloc)

## getting started

1. **Clone this repository** to a directory on your local machine:

    ```
    $ cd /path/to/your/preferred/directory
    $ git clone git@github.com:datakind/msvdd_Bloc.git
    $ cd msvdd_Bloc
    ```

1. **Create a virtual environment** to isolate our project's dependencies from your other projects'. Use whichever tool you prefer (e.g. `virtualenv`, `pyenv`, `pipenv`). Here's an example using `pyenv`:

    ```
    msvdd_Bloc(master)$ pyenv virtualenv 3.7.4 bloc-env
    msvdd_Bloc(master)$ pyenv shell bloc-env
    ```

1. **Install the package** in one of two ways.
   - If you want to use the `msvdd_bloc` code as-is without further development, installation is simple:

        ```
        (bloc-env) msvdd_Bloc(master)$ pip install .
        ```

   - If you need to further develop the code, install the package in locally-editable (aka develop) mode, plus a few additional dependencies:

        ```
        (bloc-env) msvdd_Bloc(master)$ pip install -e .
        (bloc-env) msvdd_Bloc(master)$ pip install -r requirements-dev.txt
        ```

1. **Create a branch** with a descriptive name for you to hack on, as needed:

    ```
    (bloc-env) msvdd_Bloc(master)$ git pull
    (bloc-env) msvdd_Bloc(master)$ git checkout -b my-example-branch-name
    ```

## documentation

Stand-alone doc files live under the top-level `docs/` directory and are written in [reStructured Text format](http://docutils.sourceforge.net/docs/user/rst/quickref.html). They are built using `sphinx`:

```
$ cd docs
$ make html
```

In-code docstrings follow [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings). These docstrings are automatically incorporated into the main docs via `sphinx.ext.sphinx-autodoc`. Refer to the [sphinx site](https://www.sphinx-doc.org/en/master/) for details.


## tests

Test modules live under the top-level `tests/` directory. They are run using `pytest`:

```
$ cd tests
$ pytest -vv .
```

A coverage report may additionally be generated using `pytest-cov`:

```
$ pytest -vv --cov=msvdd_bloc --cov-report=term-missing .
```

Refer to the [pytest site](https://docs.pytest.org/en/latest/) for details.
