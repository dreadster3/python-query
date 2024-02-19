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
