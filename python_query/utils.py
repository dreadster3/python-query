import inspect
from typing import Any, Dict

from python_query.types import TQueryKey


def hash_query_key(key: TQueryKey) -> str:
    if isinstance(key, str):
        key = [key]

    final_key = []
    for item in key:
        if isinstance(item, dict):
            sorted_dict = sort_dict_by_key(item)
            final_key.append(str(sorted_dict))

        else:
            final_key.append(str(item))

    return str(hash("".join(final_key)))


def sort_dict_by_key(dict_: Dict[str, Any]) -> Dict[str, Any]:
    return dict(sorted(dict_.items(), key=lambda item: item[0]))


def call_function_partial(func, args_have_self=False, *args, **kwargs):
    params = inspect.signature(func).parameters

    # If self is in the parameters and it's not in the arguments, remove it
    if args_have_self and params.get("self") is None:
        args = args[1:]

    func_args = {k: v for k, v in zip(params.keys(), args)}
    func_args.update(kwargs)

    return func(**func_args)


def is_class_method(method) -> bool:
    params = inspect.signature(method).parameters
    return params.get("self") is not None
