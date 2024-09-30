# Thingifier Tests

## How to run:

1. Make sure the Thingifier API is running, otherwise the tests will fail 
2. Go into the `thingifier-tests` directory
3. Run `poetrt install` to install all dependencies
4. Run `poetry run pytest` to run the tests

## How to write a test
1. Create a file called `test_[whatever].py` 
2. In the file, any function called `test_[whatever]()` will be run as a test when you do `poetry run pytest`. Any other function will not, e.g., helper functions and setup functions
3. You can have a class, again, it has to be called `class Test[Whatever]():`. This is just Python syntax now, but remember to put `self` as an argument if you have methods inside a class
