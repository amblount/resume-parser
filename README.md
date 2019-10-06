# msvdd_Bloc

Microsoft + DataKind AI in Cities Virtual Accelerator - DataDive

### Getting started:

1. Clone this repository to a directory on your local machine:

    ```
    $ cd /path/to/your/preferred/directory
    $ git clone git@github.com:datakind/msvdd_Bloc.git
    $ cd msvdd_Bloc
    ```

1. Add this directory to your `PYTHONPATH`:

    ```
    $ export PYTHONPATH="${PYTHONPATH}:/path/to/msvdd_Bloc/"
    ```

1. Create a virtual environment to isolate our project's dependencies from your other projects'. Use whichever tool you prefer (e.g. `virtualenv`, `pyenv`, `pipenv`). Here's an example using `pyenv`:

    ```
    msvdd_Bloc(master)$ pyenv virtualenv 3.7.4 datakind-bloc
    msvdd_Bloc(master)$ pyenv shell datakind-bloc
    ```

1. Install project dependencies:

    ```
    (datakind-bloc) msvdd_Bloc(master)$ pip install -r requirements.txt
    ```

1. Create a branch with a descriptive name for you to start hacking on:

    ```
    (datakind-bloc) msvdd_Bloc(master)$ git pull
    (datakind-bloc) msvdd_Bloc(master)$ git checkout -b burton-example-branch-name
    ```
