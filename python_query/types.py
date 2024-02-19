from collections.abc import Awaitable, Callable
from typing import Any, Dict, List, TypeVar, Union

from python_query.query_options import QueryOptions

TQueryKey = Union[str, List[Union[str, Dict[str, Any]]]]

TQueryOptions = QueryOptions | Dict[str, Any]

TData = TypeVar('TData')
TFn = Callable[[], Union[Awaitable[TData], TData]]
