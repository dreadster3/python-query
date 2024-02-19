import pytest
from python_query.query_cache import QueryCache


@pytest.mark.asyncio
async def test_query_cache():
    query_cache = QueryCache({"cache_time": 1})

    query_cache["test"] = lambda: 1

    data = await query_cache.get_query_data_async("test")

    assert data == 1


@pytest.mark.asyncio
async def test_query_cache_overwrite():
    query_cache = QueryCache({"cache_time": 1})

    query_cache["test"] = lambda: 1
    query_cache["test"] = lambda: 2

    data = await query_cache.get_query_data_async("test")

    assert data == 2


@pytest.mark.asyncio
async def test_query_cache_not_exact():
    query_cache = QueryCache({"cache_time": 1})

    query_cache[["test", "1"]] = lambda: 1  # type: ignore
    query_cache[["test", "2"]] = lambda: 2  # type: ignore

    queries = query_cache.get_queries_not_exact("test")

    assert len(queries) == 2
    assert await queries[0].fetch_async() == 1
    assert await queries[1].fetch_async() == 2
    assert queries[0].get_hash() != queries[1].get_hash()
