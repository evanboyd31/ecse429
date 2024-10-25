from behave import given, when, then

@given('I have the numbers {num1:d} and {num2:d}')
def step_given_numbers(context, num1, num2):
    context.num1 = num1
    context.num2 = num2

@when('I add the numbers')
def step_when_add_numbers(context):
    context.result = context.num1 + context.num2

@then('the result should be {expected_result:d}')
def step_then_result(context, expected_result):
    assert context.result == expected_result
