import pytest

from python_query.query_cache import QueryCache


@pytest.mark.asyncio
async def test_query_cache() -> None:
    query_cache = QueryCache({"cache_time": 1})

    query_cache["test"] = lambda: 1

    data = await query_cache.get_query_data_async("test")

    assert data == 1


@pytest.mark.asyncio
async def test_query_cache_overwrite() -> None:
    query_cache = QueryCache({"cache_time": 1})

    query_cache["test"] = lambda: 1
    query_cache["test"] = lambda: 2

    data = await query_cache.get_query_data_async("test")

    assert data == 2


@pytest.mark.asyncio
async def test_query_cache_not_exact() -> None:
    query_cache = QueryCache({"cache_time": 1})

    query_cache[["test", "1"]] = lambda: 1  # pyright: ignore
    query_cache[["test", "2"]] = lambda: 2  # pyright: ignore

    queries = query_cache.get_queries_not_exact("test")

    assert len(queries) == 2
    assert await queries[0].fetch_async() == 1
    assert await queries[1].fetch_async() == 2
    assert queries[0].get_hash() != queries[1].get_hash()


@pytest.mark.asyncio
async def test_query_cache_not_exact_complex() -> None:
    query_cache = QueryCache({"cache_time": 1})

    query_cache[["test", "1", {"page": 1}]] = lambda: 1
    query_cache[["test", "1", {"page": 1, "per_page": 10}]] = lambda: 2

    queries = query_cache.get_queries_not_exact(["test", "1", {"page": 1}])

    assert len(queries) == 2
    assert queries[0]._key == ["test", "1", {"page": 1}]
    assert queries[1]._key == ["test", "1", {"page": 1, "per_page": 10}]
    assert await queries[0].fetch_async() == 1
    assert await queries[1].fetch_async() == 2
    assert queries[0].get_hash() != queries[1].get_hash()


def test_query_cache_not_existing() -> None:
    query_cache = QueryCache({"cache_time": 1})

    assert query_cache.get_query("test") is None

    with pytest.raises(KeyError):
        query_cache["test"]


def test_decorator_sync() -> None:
    query_cache = QueryCache({"cache_time": 1})

    @query_cache.cache(["test"])
    def test() -> int:
        return 1

    assert query_cache.get_query("test") is None
    assert test() == 1

    query = query_cache.get_query("test")

    assert query is not None
    assert query._data == 1
    assert test() == 1


@pytest.mark.asyncio
async def test_decorator_async() -> None:
    query_cache = QueryCache({"cache_time": 1})

    @query_cache.cache(["test"])
    async def test() -> int:
        return 1

    assert query_cache.get_query("test") is None
    assert await test() == 1

    query = query_cache.get_query("test")

    assert query is not None
    assert query._data == 1
    assert await test() == 1
    assert await query.fetch_async() == 1
