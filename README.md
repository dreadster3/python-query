# Python Query

Python library heavily inspired by [react-query](https://react-query.tanstack.com/).

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
