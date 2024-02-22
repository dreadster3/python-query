import asyncio
import functools
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union

import nest_asyncio

import python_query.utils as utils
from python_query.query import Query
from python_query.query_options import QueryOptions
from python_query.types import TData, TQueryKey, TQueryOptions


class QueryCache:
    def __init__(
            self,
            default_options: TQueryOptions = QueryOptions()) -> None:
        self.__queries: Dict[str, Query[Any]] = {}
        self.__default_options = default_options

    def __getitem__(self, key: TQueryKey) -> Query[Any]:
        query = self.get_query(key)

        if query is None:
            raise KeyError(f"Query with key {key} not found")

        return query

    def __setitem__(self,
                    key: TQueryKey,
                    value: Callable[[],
                                    Union[Awaitable[TData],
                                          TData]]) -> None:
        self.add_query(key, value)

    def add_query(self,
                  key: TQueryKey,
                  fn: Callable[[],
                               Union[Awaitable[TData],
                                     TData]]) -> Query[TData]:
        query: Query[TData] = Query(key, fn, self.__default_options)
        self.__queries[query.get_hash()] = query
        return query

    def get_query(self, key: TQueryKey) -> Optional[Query[Any]]:
        return self.__queries.get(utils.hash_query_key(key))

    def get_queries_not_exact(self, key: TQueryKey) -> List[Query[Any]]:
        return [
            query for query in self.__queries.values() if query.matches_key(
                key, False)]

    async def get_query_data_async(self, key: TQueryKey) -> Any:
        return await self[key].fetch_async()

    TQueryKeyDecorator = TQueryKey | Callable[[], TQueryKey]

    def cache(self,
              key: TQueryKeyDecorator) -> Callable[[],
                                                   Union[Awaitable[TData],
                                                         TData]]:
        def wrapper(fn: Callable[[], Union[Awaitable[TData], TData]], *
                    args, **kwargs) -> Callable[[], Union[Awaitable[TData], TData]]:
            if asyncio.iscoroutinefunction(fn):
                @functools.wraps(fn)
                async def wrapped(*args: Any, **kwargs: Any) -> TData:
                    if callable(key):
                        final_key = key(*args, **kwargs)
                    else:
                        final_key = key

                    async def inner() -> TData:
                        return await fn(*args, **kwargs)

                    if query := self.get_query(final_key) is None:
                        query = self.add_query(
                            final_key, inner)

                    return await query.fetch_async()

            else:
                def wrapped(*args: Any, **kwargs: Any) -> TData:
                    if callable(key):
                        final_key = key(*args, **kwargs)
                    else:
                        final_key = key

                    def inner() -> TData:
                        return fn(*args, **kwargs)

                    if (query := self.get_query(final_key)) is None:
                        query = self.add_query(
                            final_key, inner)

                    loop = asyncio.get_event_loop()
                    nest_asyncio.apply(loop)
                    return loop.run_until_complete(query.fetch_async())

            return wrapped
        return wrapper

    def cache_async(self, key: TQueryKey):
        def wrapper(fn: Callable[[],
                                 Union[Awaitable[TData],
                                       TData]]) -> Callable[[],
                                                            Awaitable[TData]]:
            @ functools.wraps(fn)
            async def wrapped(*args: Any, **kwargs: Any) -> TData:
                async def inner() -> TData:
                    if isinstance(fn, Awaitable):
                        return await fn(*args, **kwargs)
                    return fn(*args, **kwargs)

                if query := self.get_query(key) is None:
                    query = self.add_query(
                        key, inner)

                return await query.fetch_async()
            return wrapped
        return wrapper
