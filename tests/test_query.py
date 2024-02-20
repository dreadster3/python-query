import pytest

from python_query.query import Query


def test_query_hash() -> None:
    query1 = Query("test", lambda: 1)
    query2 = Query("test", lambda: 2)

    assert query1.get_hash() == query2.get_hash()


def test_query_complex_hash() -> None:
    query1 = Query(["test", {"page": 1, "per_page": 2}], lambda: 1)
    query2 = Query(["test", {"per_page": 2, "page": 1}], lambda: 2)

    assert query1.get_hash() == query2.get_hash()


def test_query_match_str() -> None:
    query1 = Query("test", lambda: 1)

    assert query1.matches_key("test")


def test_query_match_list() -> None:
    query1 = Query(["test", "1"], lambda: 1)

    assert query1.matches_key(["test", "1"])


def test_query_match_list_not_exact() -> None:
    query1 = Query(["test", "1"], lambda: 1)

    assert query1.matches_key("test", False)
    assert query1.matches_key(["test"], False)
    assert query1.matches_key(["test", "1"], False)


def test_query_time_until_stale() -> None:
    query = Query("test", lambda: 1, {"cache_time": 1})
    time_until_stale = query.time_until_stale()

    assert query._cache_time == 1
    assert time_until_stale == 1


@pytest.mark.asyncio
async def test_fetch() -> None:
    query = Query("test", lambda: 1)

    before = query._updated_at
    data = await query.fetch_async()

    assert data == 1
    assert query._updated_at is not None
    assert query._updated_at > before


@pytest.mark.asyncio
async def test_refetch() -> None:
    count = 0

    def fn() -> int:
        nonlocal count
        count += 1
        return count

    query = Query("test", fn, {"cache_time": 0})

    data = await query.fetch_async()

    assert data == 1

    data2 = await query.fetch_async()

    # Should refetch
    assert data2 == 2


@pytest.mark.asyncio
async def test_norefetch() -> None:
    count = 0

    def fn() -> int:
        nonlocal count
        count += 1
        return count

    query = Query("test", fn, {"cache_time": 1})

    data = await query.fetch_async()

    assert data == 1

    data2 = await query.fetch_async()

    # Should refetch
    assert data2 == 1
