# Python Query

Python library heavily inspired by [react-query](https://tanstack.com/query/v4/).

## Getting Started

Here is a compilation of some actions that are achievable with this library.

```python
import asyncio

import python_query


async def function() -> None:
    await asyncio.sleep(1)
    return 2


async def main():
    query_cache = python_query.QueryCache()
    query_cache["query1"] = lambda: 1
    query_cache["query2"] = function

    assert await query_cache["query1"].fetch_async() == 1
    assert await query_cache["query2"].fetch_async() == 2

    query_cache["query1"] = lambda: 3

    assert await query_cache["query1"].fetch_async() == 3

    query_cache["parent", "child1", {"page": 1}] = lambda: 4
    query_cache["parent", "child1", {
        "page": 1, "per_page": 10}] = lambda: 5
    queries = query_cache.get_queries_not_exact("parent")
    queries2 = query_cache.get_queries_not_exact(["parent", "child1"])
    queries3 = query_cache.get_queries_not_exact(
        ["parent", "child1", {"page": 1}])

    assert len(queries) == 2
    assert len(queries2) == 2
    assert len(queries3) == 2


asyncio.run(main())
```

## Decorators

The library also provides decorators to easily create queries.

```python
import asyncio

import python_query

query_cache = python_query.QueryCache()


# Static keys
@query_cache.cache(["key", "1"])
async def function() -> None:
    await asyncio.sleep(1)
    return 2

# Generate keys based on the arguments
@query_cache.cache(lambda number: ["key", "1", number])
async def function2(number : int) -> None:
    await asyncio.sleep(1)
    return number


async def main():
    # Only added to cache when called first time
    assert query_cache.get_query(["key", "1"]) is None

    assert await function() == 2
    assert query_cache.get_query(["key", "1"]) is not None
    assert await query_cache.get_query(["key", "1"]).fetch_async() == 2
    assert await function() == 2


    # Only added to cache when called first time
    assert query_cache.get_query(["key", "1", 3]) is None

    assert await function2(3) == 3
    assert query_cache.get_query(["key", "1", 2]) is None
    assert query_cache.get_query(["key", "1", 3]) is not None
    assert await query_cache.get_query(["key", "1", 3]).fetch_async() == 3
    assert await function2(3) == 3


asyncio.run(main())
```
