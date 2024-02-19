import inspect
import logging
import math
from datetime import datetime
from typing import Any, Generic, Union

import python_query.utils as utils
from python_query.query_options import QueryOptions
from python_query.types import TData, TFn, TQueryKey, TQueryOptions


class NotSet:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "NotSet"


class Query(Generic[TData]):
    def __init__(self, key: TQueryKey, fn: TFn, query_options: TQueryOptions = QueryOptions()):
        if isinstance(query_options, dict):
            query_options = QueryOptions(**query_options)

        if isinstance(key, str):
            key = [key]

        self._hash = utils.hash_query_key(key)
        self._key = key
        self._fn = fn
        self._data: TData | NotSet = NotSet()
        # Cache time in seconds
        self._cache_time = query_options._cache_time
        self._updated_at = datetime.now().timestamp()
        self._logger = logging.getLogger(self.__class__.__name__)

    def time_until_stale(self) -> int:
        return math.ceil(self._cache_time - (datetime.now().timestamp() - self._updated_at))

    def get_data(self) -> Union[TData, NotSet]:
        return self._data

    def get_hash(self) -> str:
        return self._hash

    def matches_key(self, key: TQueryKey, exact: bool = True) -> bool:
        if isinstance(key, str):
            key = [key]

        if exact:
            return self._hash == utils.hash_query_key(key)

        for k1, k2 in zip(self._key, key):
            if isinstance(k1, dict) and isinstance(k2, dict):
                for k in k1.keys():
                    if k not in k2:
                        return False
                    if k1[k] != k2[k]:
                        return False
            else:
                if k1 != k2:
                    return False

        return True

    async def __fetch_async(self) -> Any:
        if inspect.iscoroutinefunction(self._fn):
            self._data = await self._fn()
        elif inspect.isfunction(self._fn):
            self._data = self._fn()
        else:
            raise ValueError(
                "Query function must be a coroutine or a regular function")

        self._updated_at = datetime.now().timestamp()
        return self._data

    async def fetch_async(self) -> TData:
        if isinstance(self._data, NotSet):
            self._logger.debug(
                f"Fetching data for %s for the first time", self._hash)
            return await self.__fetch_async()

        if self.time_until_stale() <= 0:
            self._logger.debug(
                "Data for %s is stale, fetching new data", self._hash)
            return await self.__fetch_async()

        return self._data
