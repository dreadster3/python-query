from typing import Any, Dict, List

import python_query.utils as utils
from python_query.query import Query
from python_query.query_options import QueryOptions
from python_query.types import TFn, TQueryKey, TQueryOptions


class QueryCache:
    def __init__(self, default_options: TQueryOptions = QueryOptions()) -> None:
        self.__queries: Dict[str, Query] = {}
        self.__default_options = default_options

    def __getitem__(self, key: TQueryKey) -> Query:
        return self.get_query(key)

    def __setitem__(self, key: TQueryKey, value: TFn):
        self.add_query(key, value)

    def add_query(self, key: TQueryKey, fn: TFn):
        query = Query(key, fn, self.__default_options)
        self.__queries[query.get_hash()] = query

    def get_query(self, key: TQueryKey) -> Query:
        return self.__queries[utils.hash_query_key(key)]

    def get_queries_not_exact(self, key: TQueryKey) -> List[Query]:
        return [query for query in self.__queries.values() if query.matches_key(key, False)]

    async def get_query_data_async(self, key: TQueryKey) -> Any:
        return await self[key].fetch_async()
