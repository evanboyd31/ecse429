from behave import given, when, then
import httpx


url: str = "http://localhost:4567/"


def remove_all():
    todos = httpx.get(url + "todos").json()["todos"]
    categories = httpx.get(url + "categories").json()["categories"]
    projects = httpx.get(url + "projects").json()["projects"]

    for todo in todos:
        httpx.delete(url + "todos/" + todo["id"])
    for category in categories:
        httpx.delete(url + "categories/" + category["id"])
    for project in projects:
        httpx.delete(url + "projects/" + project["id"])


@given("no objects exist in the thingifier app")
def given_no_objects_exist_in_the_thingifier_app(context):
    remove_all()


@given('the category "{string}" exists')
def given_the_category_exists(context, string):
    res = httpx.post(url + "categories", json={"title": string})
    json = res.json()
    context.category = json


@then('the todo should have the category "{string}"')
def then_the_todo_should_have_the_category(context, string):
    todo_id = context.todo["id"]
    res = httpx.get(url + "todos/" + todo_id + "/categories")
    json = res.json()
    assert json["categories"][0]["title"] == string


@when("the student assigns the category to the todo")
def when_the_student_assigns_the_category_to_the_todo(context):
    category_id = context.category["id"]
    todo_id = context.todo["id"]
    res = httpx.post(url + "todos/" + todo_id + "/categories", json={"id": category_id})
    context.response = res


@given('the todo "{string}" exists')
def given_the_todo_exists(context, string):
    res = httpx.post(url + "todos", json={"title": string})
    json = res.json()
    context.todo = json


@then("the todo should be created")
def then_the_todo_should_be_created(context):
    todo_id = context.todo["id"]
    res = httpx.get(url + "todos/" + todo_id)
    assert res.status_code == 200


@then('the thingifier app should return an error message containing "{string}"')
def then_the_thingifier_app_should_return_an_error_message_containing(context, string):
    # DELETE THIS
    assert string in context.response.json()["errorMessages"][0]


@when("the student assigns the project to the todo")
def when_the_student_assigns_the_project_to_the_todo(context):
    todo_id = context.todo["id"]
    project_id = context.project["id"]
    res = httpx.post(url + "todos/" + todo_id + "/tasksof", json={"id": project_id})
    context.response = res


@then('the project should have the todo "{string}"')
def then_the_project_should_have_the_todo(context, string):
    project_id = context.project["id"]
    res = httpx.get(url + "projects/" + project_id + "/tasks")
    json = res.json()
    assert json["todos"][0]["title"] == string


@then('the todo should have the project "{string}"')
def then_the_todo_should_have_the_project(context, string):
    todo_id = context.todo["id"]
    res = httpx.get(url + "todos/" + todo_id + "/tasksof")
    json = res.json()
    assert json["projects"][0]["title"] == string


@when('the student creates a todo with title "{string}" with that project')
def when_the_student_creates_a_todo_with_title_with_that_project(context, string):
    project_id = context.project["id"]
    res = httpx.post(
        url + "todos", json={"title": string, "tasksof": [{"id": project_id}]}
    )
    context.response = res
    context.todo = res.json()


@given('the project "{string}" exists')
def given_the_project_exists(context, string):
    res = httpx.post(url + "projects", json={"title": string})
    json = res.json()
    context.project = json


@when("the student assigns the todo to the project")
def when_the_student_assigns_the_todo_to_the_project(context):
    todo_id = context.todo["id"]
    project_id = context.project["id"]
    res = httpx.post(url + "todos/" + todo_id + "/tasksof", json={"id": project_id})
    context.response = res


@when("the student deletes the todo")
def when_the_student_deletes_the_todo(context):
    todo_id = context.todo["id"]
    res = httpx.delete(url + "todos/" + todo_id)
    context.response = res


@given("the todo is assigned to the project")
def given_the_todo_is_assigned_to_the_project(context):
    project_id = context.project["id"]
    todo_id = context.todo["id"]
    res = httpx.post(url + "todos/" + todo_id + "/tasksof", json={"id": project_id})


@then('the project should not have the todo "{string}"')
def then_the_project_should_not_have_the_todo(context, string):
    project_id = context.project["id"]
    res = httpx.get(url + "projects/" + project_id + "/tasks")
    json = res.json()
    todos = json["todos"]
    for todo in todos:
        if todo["title"] == string:
            assert False


@then('the todo should not have the project "{string}"')
def then_the_todo_should_not_have_the_project(context, string):
    todo_id = context.todo["id"]
    res = httpx.get(url + "todos/" + todo_id + "/tasksof")
    json = res.json()
    projects = json["projects"]
    for project in projects:
        if project["title"] == string:
            assert False


@when("the todo is removed from the project")
def when_the_todo_is_removed_from_the_project(context):
    todo_id = context.todo["id"]
    project_id = context.project["id"]
    res = httpx.delete(url + "projects/" + project_id + "/tasks/" + todo_id)
    context.response = res


@when("the category is removed from the todo")
def when_the_category_is_removed_from_the_todo(context):
    todo_id = context.todo["id"]
    category_id = context.category["id"]
    res = httpx.delete(url + "todos/" + todo_id + "/categories/" + category_id)
    context.response = res


@then('the todo should not have the category "{string}"')
def then_the_todo_should_not_have_the_category(context, string):
    todo_id = context.todo["id"]
    res = httpx.get(url + "todos/" + todo_id + "/categories")
    json = res.json()
    categories = json["categories"]
    for category in categories:
        if category["title"] == string:
            assert False


@then('the thingifier app should return a response with status code "{statusCode}"')
def step_the_thingifier_app_should_return_the_error_status(context, statusCode):
    # DELETE THIS
    print(context.response.status_code, "\n")
    assert context.response.status_code == int(statusCode)


@when("the student deletes the category")
def when_the_student_deletes_the_category(context):
    category_id = context.category["id"]
    res = httpx.delete(url + "categories/" + category_id)
    context.response = res


@given("the category is assigned to the todo")
def given_the_category_is_assigned_to_the_todo(context):
    category_id = context.category["id"]
    todo_id = context.todo["id"]
    res = httpx.post(url + "todos/" + todo_id + "/categories", json={"id": category_id})


@when("the student assigns the category to the project")
def when_the_student_assigns_the_category_to_the_project(context):
    project_id = context.project["id"]
    category_id = context.category["id"]
    res = httpx.post(
        url + "projects/" + project_id + "/categories", json={"id": category_id}
    )
    context.response = res


@then('the project should have the category "{string}"')
def then_the_project_should_have_the_category(context, string):
    project_id = context.project["id"]
    res = httpx.get(url + "projects/" + project_id + "/categories")
    json = res.json()
    assert json["categories"][0]["title"] == string


@then("the project should be created")
def then_the_project_should_be_created(context):
    project_id = context.project["id"]
    res = httpx.get(url + "projects/" + project_id)
    assert res.status_code == 200


@when('the student creates a todo with title "{string}" with that category')
def step_when_the_student_creates_a_todo_with_title_with_that_category(context, string):
    category_id = context.category["id"]
    res = httpx.post(
        url + "todos", json={"title": string, "categories": [{"id": category_id}]}
    )
    context.response = res
    context.todo = res.json()


@when('the student creates a project with title "{string}" with that category')
def when_the_student_creates_a_project_with_title_with_the_category(context, string):
    category_id = context.category["id"]
    res = httpx.post(
        url + "projects", json={"title": string, "categories": [{"id": category_id}]}
    )
    context.response = res
    context.project = res.json()


@when("the student assigns a non-existent category to the todo")
def step_the_student_assigns_a_non_existent_category_to_the_todo(context):
    todo_id = context.todo["id"]
    res = httpx.post(url + "todos/" + todo_id + "/categories", json={"id": -1})
    context.response = res


@when("the student assigns a non-existent project to the todo")
def step_the_student_assigns_a_non_existent_project_to_the_todo(context):
    todo_id = context.todo["id"]
    res = httpx.post(url + "todos/" + todo_id + "/tasksof", json={"id": -1})
    context.response = res


@when("the student assigns a non-existent category to the project")
def step_the_student_assigns_a_non_existent_category_to_the_project(context):
    project_id = context.project["id"]
    res = httpx.post(url + "projects/" + project_id + "/categories", json={"id": -1})
    context.response = res


@when("the student deletes a non-existent todo from the project")
def step_the_student_deletes_a_non_existent_todo_from_the_project(context):
    project_id = context.project["id"]
    res = httpx.delete(url + "projects/" + project_id + "/tasks/-1")
    context.response = res


@when("the student deletes a non-existent category from the todo")
def step_the_student_deletes_a_non_existent_category_from_the_todo(context):
    todo_id = context.todo["id"]
    res = httpx.delete(url + "todos/" + todo_id + "/categories/-1")
    context.response = res
