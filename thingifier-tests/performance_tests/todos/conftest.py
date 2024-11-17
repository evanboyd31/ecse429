import time
import httpx
import pytest
import thingifier_tests.conftest as common
import xmltodict
import copy

todos_url: str = "http://localhost:4567/todos"
XML_HEADERS = {"Content-Type": "application/xml", "Accept": "application/xml"}


def xml_to_dict(xml: str) -> dict:
    return xmltodict.parse(xml)


# Note that ids will change every time
default_todos: dict = {
    "todos": [
        {
            "id": "???",
            "title": "Watch Sabrina Carpenter Concert Clips",
            "doneStatus": "false",
            "description": "Watch them on TikTok",
        },
        {
            "id": "???",
            "title": "Buy Sabrina Carpenter Merch",
            "doneStatus": "false",
            "description": "Get shirt H",
        },
        {
            "id": "???",
            "title": "Buy Sabrina Carpenter Concert Tickets",
            "doneStatus": "false",
            "description": "They are sold out sadly",
        },
    ]
}


def get_default_todos_for_xml() -> dict:
    out = {"todo": []}
    for todo in default_todos["todos"]:
        copied = copy.deepcopy(todo)
        if copied["description"] == "":
            copied["description"] = None
        out["todo"].append(copied)
    return out


def contain_the_same_todos(todos1, todos2) -> bool:
    if "todos" in todos1:
        todos1 = todos1["todos"]
    elif "todo" in todos1:
        todos1 = todos1["todo"]

    if "todos" in todos2:
        todos2 = todos2["todos"]
    elif "todo" in todos2:
        todos2 = todos2["todo"]
    print(todos1)
    print(todos2)

    todos1 = sorted(todos1, key=lambda todo: todo["id"])
    todos2 = sorted(todos2, key=lambda todo: todo["id"])
    return todos1 == todos2


def todos_has_not_changed() -> bool:
    res = httpx.get(todos_url)
    actual = res.json()
    return res.status_code == 200 and contain_the_same_todos(actual, default_todos)


@pytest.fixture(autouse=True)
def before_each():
    if common.make_sure_system_ready() != True:
        print("The system is not ready to be tested.")
        assert False
    common.remove_all()
    for todo in default_todos["todos"]:
        todo.pop("id")
        todo["doneStatus"] = False
        res = httpx.post(todos_url, json=todo)
        todo["doneStatus"] = "false"
        todo["id"] = res.json()["id"]

    start_time = time.time()  # Record the start time

    yield
    
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Test execution time: {execution_time:.2f} seconds")
