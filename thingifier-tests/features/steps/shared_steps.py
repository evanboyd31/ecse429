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

@then('the thingifier app should return an error message containing "{string}"')
def step_then(context, string):
    assert string in context.response.json().get("errorMessages")[0]

def remove_all():
    response = httpx.get(url + "todos")
    assert response.status_code == 200
    for todo in response.json()["todos"]:
        deleteResponse = httpx.delete(url + "todos/" + str(todo["id"]))
        assert deleteResponse.status_code == 200

    response = httpx.get(url + "categories")
    assert response.status_code == 200
    for category in response.json()["categories"]:
        deleteResponse = httpx.delete(url + "categories/" + str(category["id"]))
        assert deleteResponse.status_code == 200

    response = httpx.get(url + "projects")
    assert response.status_code == 200
    for project in response.json()["projects"]:
        deleteResponse = httpx.delete(url + "projects/" + str(project["id"]))
        assert deleteResponse.status_code == 200

@then('the thingifier app should return the error status "{statusCode}"')
def step_thingifier_app_should_return_the_error_status(context, statusCode):
    assert context.response.status_code == int(statusCode)

@then('the thingifier app should return a response with status code "{statusCode}"')
def step_thingifier_app_should_return_a_response_with_status_code(context, statusCode):
    assert context.response.status_code == int(statusCode)