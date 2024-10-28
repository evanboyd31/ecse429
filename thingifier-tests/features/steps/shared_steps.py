from behave import given, when, then
import httpx

url: str = "http://localhost:4567/"


@given("the thingifier application is running")
def step_given_the_thingifier_application_is_running(context):
    try:
        response = httpx.get(url + "todos")
        if response.status_code != 200:
            assert False
    except httpx.ConnectError:
        assert False
