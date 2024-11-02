import httpx
import parse
import xmltodict

from behave import given, when, then, register_type
from shared_steps import url, remove_all, XML_HEADERS

todos_url = f"{url}todos"


@parse.with_pattern(r".*")
def parse_nullable_string(text):
    return text


register_type(NullableString=parse_nullable_string)


@given("no objects exist other than the following todos in the thingifier application")
def step_given_no_objects_exist_other_than_the_following_todos_in_the_thingifier_application(
    context,
):
    remove_all()
    context.todos = {}

    for row in context.table:
        todoResponse = create_todo(row["title"], row["doneStatus"], row["description"])
        context.todos[row["title"]] = todoResponse.json()


@when(
    'the student sends a POST API request for the "/todos" endpoint with json body containing title "{title:NullableString}" done status "{doneStatus:NullableString}" and description "{description:NullableString}"'
)
def step_when_the_student_sends_a_POST_API_request_for_the_todos_endpoint_json(
    context, title, doneStatus, description
):
    todoResponse = create_todo(title, doneStatus, description)
    context.response = todoResponse


@then(
    'the thingifier app should return a response containing the todo with title "{title:NullableString}" done status "{doneStatus:NullableString}" and description "{description:NullableString}"'
)
def step_then_the_thingifer_app_should_return_a_response_containing(
    context, title, doneStatus, description
):
    todo = extract_todo_response(context.response)
    assert todo["title"] == title
    assert todo["doneStatus"] == doneStatus
    assert todo["description"] == description


@then(
    'the thingifier app should contain the todo with title "{title:NullableString}" done status "{doneStatus:NullableString}" and description "{description:NullableString}"'
)
def step_then_the_thingifer_app_should_contain(context, title, doneStatus, description):
    todos = fetch_all_todos()
    contains = False
    for todo in todos:
        if (
            todo["title"] == title
            and todo["doneStatus"] == doneStatus
            and todo["description"] == description
        ):
            contains = True
    assert contains


@when(
    'the student sends a POST API request for the "/todos" endpoint with xml body containing title "{title:NullableString}" done status "{doneStatus:NullableString}" and description "{description:NullableString}"'
)
def step_when_the_student_sends_a_POST_API_request_for_the_todos_endpoint_xml(
    context, title, doneStatus, description
):
    context.response = create_todo(title, doneStatus, description, False)


@then(
    'the thingifier app should not contain a todo with title "{title:NullableString}"'
)
def step_then_the_thingifer_app_should_not_contain(context, title):
    todos = fetch_all_todos()
    contains = False
    for todo in todos:
        if todo["title"] == title:
            contains = True
    assert not contains


@when(
    'the student sends a DELETE API requests for the "/todos/:id" endpoint with the id of the todo with title "{title:NullableString}"'
)
def step_when_the_student_sends_a_DELETE_API_request(context, title):
    todoID = context.todos[title]["id"]
    todoResponse = httpx.delete(f"{todos_url}/{todoID}")
    context.response = todoResponse


@when(
    'the student sends a DELETE API request for the "/todos/:id" endpoint with the id of the todo with title "{title:NullableString}" and extra query parameters "{queryParams:NullableString}"'
)
def step_when_the_student_sends_a_DELETE_API_request_with_queryParams(
    context, title, queryParams
):
    todoID = context.todos[title]["id"]
    todoResponse = httpx.delete(f"{todos_url}/{todoID}{queryParams}")
    context.response = todoResponse


@when(
    'the student sends a DELETE API request for the todo with id "{id:NullableString}"'
)
def step_when_the_student_sends_a_DELETE_API_request_with_id(context, id):
    todoResponse = httpx.delete(f"{todos_url}/{id}")
    context.response = todoResponse


@when(
    'the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "{title:NullableString}", and with json body containing doneStatus "{doneStatus:NullableString}"'
)
def step_when_the_student_sends_a_POST_API_request_for_the_status_json(
    context, title, doneStatus
):
    todoID = context.todos[title]["id"]
    todoResponse = update_todo(todoID, doneStatus=doneStatus)
    context.response = todoResponse


@then(
    'the thingifier app should have the todo with title "{title:NullableString}" marked as done'
)
def step_then_the_thingifer_app_should_not_contain(context, title):
    todos = fetch_all_todos()
    marked = False
    for todo in todos:
        if todo["title"] == title:
            marked = todo["doneStatus"] == "true"
    assert marked


@when(
    'the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "{title:NullableString}", and with xml body containing doneStatus "{doneStatus:NullableString}"'
)
def step_when_the_student_sends_a_POST_API_request_for_the_status_xml(
    context, title, doneStatus
):
    todoID = context.todos[title]["id"]
    todoResponse = update_todo(todoID, doneStatus=doneStatus, isJson=False)
    context.response = todoResponse


@when(
    'the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "{originalTitle:NullableString}", and with json body containing title "{title:NullableString}", and description "{description:NullableString}"'
)
def step_when_the_student_sends_a_POST_API_request_for_the_details_json(
    context, originalTitle, title, description
):
    todoID = context.todos[originalTitle]["id"]
    todoResponse = update_todo(todoID, title=title, description=description)
    context.response = todoResponse


@when(
    'the student sends a POST API request for the "/todos/:id" endpoint with the id of the todo with title "{originalTitle:NullableString}", and with xml body containing title "{title:NullableString}", and description "{description:NullableString}"'
)
def step_when_the_student_sends_a_POST_API_request_for_the_details_xml(
    context, originalTitle, title, description
):
    todoID = context.todos[originalTitle]["id"]
    todoResponse = update_todo(
        todoID, title=title, description=description, isJson=False
    )
    context.response = todoResponse


@when('the student sends a GET API request for the "/todos?doneStatus=false" endpoint')
def step_when_the_student_sends_a_GET_API_request_unfinished(context):
    todoResponse = fetch_todos_filter("?doneStatus=false")
    context.response = todoResponse


@when(
    'the student sends a GET API request for the "/todos?doneStatus=false" endpoint with the additional query parameters "{queryParams:NullableString}"'
)
def step_when_the_student_sends_a_GET_API_request_unfinished_queryParams(
    context, queryParams
):
    todoResponse = fetch_todos_filter(f"?doneStatus=false{queryParams}")
    context.response = todoResponse


@then(
    'the thingifier app should return a response containing the list of todos "{todosList:NullableString}"'
)
def step_then_the_thingifer_app_should_return_a_response_containing_list(
    context, todosList
):
    todos = extract_todo_response(context.response)["todos"]
    listTD = todosList.split(",")
    allTodosInResponseAreAlsoInListTD = True

    for todo in todos:
        if todo["title"] in listTD:
            listTD.remove(todo["title"])
        else:
            allTodosInResponseAreAlsoInListTD = False

    assert allTodosInResponseAreAlsoInListTD
    assert not listTD or listTD == [""]


@then(
    'the thingifier app should return a response containing the unfinished todo with title "{title:NullableString}" and description "{description:NullableString}"'
)
def step_then_the_thingifer_app_should_return_a_response_containing_unfinished(
    context, title, description
):
    todo = extract_todo_response(context.response)["todos"][0]
    assert todo["title"] == title
    assert todo["description"] == description


@when(
    'the student sends a GET API request for the "/todos?doneStatus=faultyBoolean" endpoint with the faulty boolean value "{faultyBoolean:NullableString}"'
)
def step_when_the_student_sends_a_GET_API_request_unfinished_faulty(
    context, faultyBoolean
):
    todoResponse = fetch_todos_filter(f"?doneStatus={faultyBoolean}")
    context.response = todoResponse


""" HELPER FUNCTIONS """


def create_todo(title: str, doneStatus: str, description: str, isJson: bool = True):
    args = {}
    doneStatus = (
        doneStatus == "true"
        if doneStatus == "false" or doneStatus == "true"
        else doneStatus
    )
    if isJson:
        body = {
            "title": title,
            "doneStatus": doneStatus,
            "description": description,
        }
        args["json"] = body
    else:
        body = f"""<todo>
            <title>{title}</title>
            <description>{description}</description>
            <doneStatus>{doneStatus}</doneStatus>
        </todo>"""
        args["content"] = body
        args["headers"] = XML_HEADERS
    return httpx.post(todos_url, **args)


def fetch_todo(id: str):
    todoResponse = httpx.get(f"{todos_url}/{id}")
    return todoResponse.headers.json()


def fetch_all_todos():
    todoResponse = httpx.get(todos_url)
    return todoResponse.json()["todos"]


def extract_todo_response(response):
    responseType = response.headers["Content-Type"]
    if "json" in responseType:
        return response.json()
    else:
        return xmltodict.parse(response.content)["todo"]


def update_todo(
    id: str,
    title: str = None,
    doneStatus: str = None,
    description: str = None,
    isJson: bool = True,
):
    args = {}
    if doneStatus != None:
        doneStatus = (
            doneStatus == "true"
            if doneStatus == "false" or doneStatus == "true"
            else doneStatus
        )
    if isJson:
        body = {}
        if title != None:
            body["title"] = title
        if doneStatus != None:
            body["doneStatus"] = doneStatus
        if description != None:
            body["description"] = description
        args["json"] = body
    else:
        body = f"""<todo>
            {f'<title>{title}</title>' if title != None else ''}
            {f'<doneStatus>{doneStatus}</doneStatus>' if doneStatus != None else ''}
            {f'<description>{description}</description>' if description != None else ''}
        </todo>"""
        args["content"] = body
        args["headers"] = XML_HEADERS

    return httpx.post(f"{todos_url}/{id}", **args)


def fetch_todos_filter(filter: str):
    todoResponse = httpx.get(f"{todos_url}{filter}")
    return todoResponse
