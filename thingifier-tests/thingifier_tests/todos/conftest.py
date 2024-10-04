import httpx
import pytest
import thingifier_tests.conftest as common
import xmltodict

todos_url: str = "http://localhost:4567/todos"


def post_xml(url, data) -> httpx.Response:
    return httpx.post(
        url,
        content=data,
        headers={"Content-Type": "application/xml", "Accept": "application/xml"},
    )


def xml_to_dict(xml: str) -> dict:
    return xmltodict.parse(xml)


# Note that ids will change every time
default_todos: dict = {
    "todos": [
        {
            "id": "???",
            "title": "Watch Sabrina Carpenter Concert Clips",
            "doneStatus": "false",
            "description": "",
        },
        {
            "id": "???",
            "title": "Buy Sabrina Carpenter Merch",
            "doneStatus": "false",
            "description": "",
        },
        {
            "id": "???",
            "title": "Buy Sabrina Carpenter Concert Tickets",
            "doneStatus": "false",
            "description": "",
        },
    ]
}


def contain_the_same_todos(todos1, todos2) -> bool:
    todos1 = todos1["todos"]
    todos2 = todos2["todos"]

    todos1 = sorted(todos1, key=lambda todo: todo["id"])
    todos2 = sorted(todos2, key=lambda todo: todo["id"])
    return todos1 == todos2


@pytest.fixture(autouse=True)
def before_each():
    common.remove_all()
    titles: list[str] = [
        "Watch Sabrina Carpenter Concert Clips",
        "Buy Sabrina Carpenter Merch",
        "Buy Sabrina Carpenter Concert Tickets",
    ]

    def add_to_todos(title: str):
        res = httpx.post(todos_url, json={"title": title})
        todo = list(
            filter(lambda todo: todo["title"] == title, default_todos["todos"])
        )[0]
        todo["id"] = res.json()["id"]

    for title in titles:
        add_to_todos(title)
