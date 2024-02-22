from collections.abc import Awaitable, Callable
from typing import Any, Dict, List, ParamSpec, TypeVar, Union

from python_query.query_options import QueryOptions

TQueryKey = Union[str, List[Union[str, Dict[str, Any]]]]

TQueryOptions = QueryOptions | Dict[str, Any]

TData = TypeVar('TData')
TFn = Callable[[], Union[Awaitable[TData], TData]]

# Decorator types
TParam = ParamSpec("TParam")
TRetType = TypeVar("TRetType")

TQueryKeyDecorator = TQueryKey | Callable[..., TQueryKey]
TFunc = Callable[TParam, TRetType]
TFunctionDecorator = Callable[[
    TFunc[TParam, TRetType]], TFunc[TParam, TRetType]]
