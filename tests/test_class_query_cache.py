
from python_query.query_cache import QueryCache


def test_class_cache() -> None:
    class TestClass:
        def __init__(self) -> None:
            self.query_cache = QueryCache()

        @QueryCache.cache(lambda self: self.query_cache, ["test", "0"])
        def test_method(self) -> int:
            return 0

        @QueryCache.cache(lambda self: self.query_cache,
                          lambda number: ["test", str(number)])
        def test_method2(self, number: int) -> int:
            return number

    test_class = TestClass()

    assert test_class.test_method() == 0
    assert test_class.test_method2(1) == 1

    print(test_class.query_cache.get_query(["test", "1"]))

    assert test_class.query_cache.get_query(["test", "0"]) is not None
    assert test_class.query_cache.get_query(["test", str(1)]) is not None
    assert test_class.query_cache.get_query(["test", str(2)]) is None


def test_class_properties_cache() -> None:
    class TestClass:
        def __init__(self) -> None:
            self.query_cache = QueryCache()
            self.root = "test"

        @QueryCache.cache(lambda self: self.query_cache,
                          lambda self: [self.root, "0"])
        def test_method(self) -> int:
            return 0

        @QueryCache.cache(lambda self: self.query_cache,
                          lambda self, number: [self.root, str(number)])
        def test_method2(self, number: int) -> int:
            return number

    test_class = TestClass()

    assert test_class.test_method() == 0
    assert test_class.test_method2(1) == 1

    print(test_class.query_cache.get_query([test_class.root, "1"]))

    assert test_class.query_cache.get_query(
        [test_class.root, "0"]) is not None
    assert test_class.query_cache.get_query(
        [test_class.root, str(1)]) is not None
    assert test_class.query_cache.get_query(
        [test_class.root, str(2)]) is None
