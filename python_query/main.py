import asyncio
import logging

from python_query.query_cache import QueryCache

logging.basicConfig(level=logging.DEBUG)

query_cache = QueryCache({"cache_time": 10})


@query_cache.cache(["test"])
async def test() -> int:
    return 1


@query_cache.cache(lambda number: ["test2", str(number)])
def test2(number: int) -> int:
    return number


async def main():

    # print(await test())
    print(test2(3))
    print(test2(3))
    print(test2(1))
    print(test2(1))

    # query = query_cache["test"]
    # query2 = query_cache["test2"]

    # print(query.get_data())
    # print(query2.get_data())

asyncio.run(main())
