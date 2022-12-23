import asyncio
import csv

import elasticsearch

# fmt: off
from backend.service.config import app  # isort: skip
from backend.service.mapping import (
    elastic_text_settings,
    mapping_for_index,
)  # isort: skip
# fmt: on

async def create_elastic_index(name) -> None:
    """creates index in elastic by name"""
    elastic_client = app.state.elastic_client
    elastic_client.indices.create(
        index=name,
        mappings=mapping_for_index,
        settings=elastic_text_settings,
    )


async def elastic_insert(index_name: str, insert_data: dict) -> None:
    """insert data into elastic index"""
    app.state.elastic_client.index(index=index_name, document=insert_data)


def get_tuple_from_csv():
    """number, message"""
    with open("posts.csv", "r", newline="", encoding="utf-8") as csvfile:
        docreader = csv.reader(csvfile)
        next(docreader)
        for row in docreader:
            yield row


def fake_get_tuple():
    data = [
        (1, "образец поискового запроса 1"),
        (2, "текст на русском, админ не проверял"),
        (3, "образ этого текста отпечатался сам"),
        (4, "преобразован администратором")
    ]
    for tuple_ in data:
        yield tuple_


async def main():
    index_name = "map"
    try:
        await create_elastic_index(index_name)
    except elasticsearch.exceptions.RequestError as ex:
        if ex.error == "resource_already_exists_exception":
            print("Index already exists")
            pass  # Index already exists. Ignore.
        else:  # Other exception - raise it
            raise ex

    # for number, message in get_tuple_from_csv():
    for number, message in fake_get_tuple():
        data = {"id": number, "message": message}
        await elastic_insert(index_name, data)


if __name__ == "__main__":
    asyncio.run(main())
