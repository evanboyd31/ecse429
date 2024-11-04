# Thingifier Tests

## How to run Gherkin feature tests (Part B):

1. Make sure the Thingifier API is running, otherwise the tests will fail
2. cd into the `thingifier-tests` directory: `cd thingifier-tests`
3. Make sure you have installed the poetry module: `pip install poetry`
4. Run `poetry install` to install all dependencies
5. Run `poetry run behave` to run the tests in order. Run `poetry run python random_behave.py` to run the Gherkin feature tests in a random order.

## How to run unit tests (Part A):

1. Make sure the Thingifier API is running, otherwise the tests will fail 
2. Go into the `thingifier-tests` directory
3. Run `poetry install` to install all dependencies
4. Run `poetry run pytest` to run the tests. Run `poetry run pytest --random-order` to run the tests in a random order

## How to write a test
1. Create a file called `test_[whatever].py` 
2. In the file, any function called `test_[whatever]()` will be run as a test when you do `poetry run pytest`. Any other function will not, e.g., helper functions and setup functions
3. You can have a class, again, it has to be called `class Test[Whatever]():`. This is just Python syntax now, but remember to put `self` as an argument if you have methods inside a class

## DevTools
### Auto rerun changed tests
`poetry run ptw [optional folder or file else it runs for the whole test suite] --runner "pytest --testmon"` runs a script that,every time a file is changed, will run previously failed tests and tests that are affected by the file change

### Formatter
`poetry run black [file/folder]` to format code in that file or folder