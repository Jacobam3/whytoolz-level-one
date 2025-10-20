"""
Part III Tests: Functions & Dictionaries - Composition and Transformation

These tests cover higher-order functions (functions that take/return functions)
and immutable dictionary operations.
"""

from tests.test_framework import TestRunner, get_runner, create_runner
import sys

# Import the module students will implement
try:
    from src import whytoolz as wt
except ImportError:
    from types import ModuleType
    wt = ModuleType('whytoolz')
    sys.modules['whytoolz'] = wt

# Get the global test runner
runner = get_runner() or create_runner()

# Special value for fill-in-the-blank tests
FILL_ME_IN = "Fill this value in"


@runner.describe("Part III: Functions & Dictionaries")
def test_part3():
    """Tests for function composition and dictionary operations"""

    # ========================================================================
    # pipe
    # ========================================================================

    @runner.it("pipe should thread data through functions left-to-right")
    def test_pipe_basic():
        result = wt.pipe(3, lambda x: x * 2, lambda x: x + 1)
        assert result == 7  # 3 * 2 = 6, 6 + 1 = 7

    @runner.it("pipe should work with more than two functions")
    def test_pipe_multiple():
        result = wt.pipe(5, lambda x: x + 1, lambda x: x * 2, lambda x: x - 3)
        assert result == FILL_ME_IN  # 5 + 1 = 6, 6 * 2 = 12, 12 - 3 = 9

    @runner.it("pipe should work with built-in functions")
    def test_pipe_builtins():
        result = wt.pipe([1, 2, 3], sum, lambda x: x * 2)
        assert result == 12  # sum([1,2,3]) = 6, 6 * 2 = 12

    @runner.it("pipe should work with no functions (return data unchanged)")
    def test_pipe_no_funcs():
        result = wt.pipe(5)
        assert result == 5

    @runner.it("pipe should work with one function")
    def test_pipe_one_func():
        result = wt.pipe(10, lambda x: x / 2)
        assert result == 5.0

    # ========================================================================
    # compose
    # ========================================================================

    @runner.it("compose should create a new function that applies funcs right-to-left")
    def test_compose_basic():
        double = lambda x: x * 2
        add_one = lambda x: x + 1
        f = wt.compose(add_one, double)  # add_one(double(x))
        assert f(3) == 7  # double(3) = 6, add_one(6) = 7

    @runner.it("compose should work with three functions")
    def test_compose_three():
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        square = lambda x: x ** 2
        f = wt.compose(add_one, double, square)  # add_one(double(square(x)))
        assert f(3) == FILL_ME_IN  # square(3) = 9, double(9) = 18, add_one(18) = 19

    @runner.it("compose should return a callable function")
    def test_compose_callable():
        f = wt.compose(lambda x: x + 1, lambda x: x * 2)
        assert callable(f)

    @runner.it("compose should work with built-in functions")
    def test_compose_builtins():
        f = wt.compose(str, len)  # str(len(x))
        result = f([1, 2, 3, 4, 5])
        assert result == '5'

    # ========================================================================
    # complement
    # ========================================================================

    @runner.it("complement should return opposite boolean result")
    def test_complement_basic():
        is_even = lambda x: x % 2 == 0
        is_odd = wt.complement(is_even)
        assert is_odd(3) is True
        assert is_odd(4) is False

    @runner.it("complement should work with truthy/falsy values")
    def test_complement_truthy():
        is_truthy = lambda x: bool(x)
        is_falsy = wt.complement(is_truthy)
        assert is_falsy(0) is True
        assert is_falsy(1) is False
        assert is_falsy([]) is FILL_ME_IN  # True

    @runner.it("complement should return a callable")
    def test_complement_callable():
        f = wt.complement(lambda x: x > 0)
        assert callable(f)

    @runner.it("complement should work with functions that take multiple args")
    def test_complement_multi_arg():
        is_greater = lambda x, y: x > y
        is_not_greater = wt.complement(is_greater)
        assert is_not_greater(5, 3) is False
        assert is_not_greater(2, 5) is True

    # ========================================================================
    # do
    # ========================================================================

    @runner.it("do should call function and return original value")
    def test_do_basic():
        result = wt.do(lambda x: x * 2, 5)
        assert result == 5  # Returns original, not doubled

    @runner.it("do should execute function for side effects")
    def test_do_side_effects():
        side_effect_tracker = []

        def record(x):
            side_effect_tracker.append(x * 2)

        result = wt.do(record, 5)
        assert result == 5
        assert side_effect_tracker == [10]

    @runner.it("do should work in a pipe")
    def test_do_in_pipe():
        log = []

        result = wt.pipe(
            5,
            lambda x: x * 2,  # 10
            lambda x: wt.do(lambda v: log.append(v), x),  # log 10, return 10
            lambda x: x + 1  # 11
        )

        assert result == 11
        assert log == [10]

    # ========================================================================
    # memoize
    # ========================================================================

    @runner.it("memoize should return a function")
    def test_memoize_returns_func():
        f = wt.memoize(lambda x: x * 2)
        assert callable(f)

    @runner.it("memoize should produce same results as original function")
    def test_memoize_correctness():
        original = lambda x: x * 2
        memoized = wt.memoize(original)
        assert memoized(5) == original(5)
        assert memoized(10) == original(10)

    @runner.it("memoize should cache results (not call function twice for same args)")
    def test_memoize_caches():
        call_count = [0]

        def expensive(x):
            call_count[0] += 1
            return x * 2

        fast = wt.memoize(expensive)

        result1 = fast(5)
        assert call_count[0] == 1

        result2 = fast(5)  # Should be cached
        assert call_count[0] == 1  # Should NOT increment
        assert result2 == result1

    @runner.it("memoize should cache different arguments separately")
    def test_memoize_different_args():
        call_count = [0]

        def expensive(x):
            call_count[0] += 1
            return x * 2

        fast = wt.memoize(expensive)

        fast(5)   # First call with 5
        fast(10)  # First call with 10
        fast(5)   # Cached call with 5

        assert call_count[0] == FILL_ME_IN  # 2 (once for 5, once for 10)

    @runner.it("memoize should work with multiple arguments")
    def test_memoize_multi_args():
        call_count = [0]

        def add(a, b):
            call_count[0] += 1
            return a + b

        fast = wt.memoize(add)

        fast(2, 3)  # First call
        fast(2, 3)  # Should be cached

        assert call_count[0] == 1

    # ========================================================================
    # assoc
    # ========================================================================

    @runner.it("assoc should return new dict with key-value added")
    def test_assoc_add():
        result = wt.assoc({'a': 1}, 'b', 2)
        assert result == {'a': 1, 'b': 2}

    @runner.it("assoc should update existing key")
    def test_assoc_update():
        result = wt.assoc({'a': 1, 'b': 2}, 'b', 3)
        assert result == FILL_ME_IN  # {'a': 1, 'b': 3}

    @runner.it("assoc should not modify original dictionary")
    def test_assoc_immutable():
        original = {'a': 1}
        result = wt.assoc(original, 'b', 2)
        assert original == {'a': 1}  # Unchanged
        assert result == {'a': 1, 'b': 2}

    @runner.it("assoc should work with empty dict")
    def test_assoc_empty():
        result = wt.assoc({}, 'a', 1)
        assert result == {'a': 1}

    # ========================================================================
    # dissoc
    # ========================================================================

    @runner.it("dissoc should remove single key")
    def test_dissoc_single():
        result = wt.dissoc({'a': 1, 'b': 2, 'c': 3}, 'b')
        assert result == {'a': 1, 'c': 3}

    @runner.it("dissoc should remove multiple keys")
    def test_dissoc_multiple():
        result = wt.dissoc({'a': 1, 'b': 2, 'c': 3}, 'a', 'c')
        assert result == FILL_ME_IN  # {'b': 2}

    @runner.it("dissoc should not modify original dictionary")
    def test_dissoc_immutable():
        original = {'a': 1, 'b': 2}
        result = wt.dissoc(original, 'a')
        assert original == {'a': 1, 'b': 2}  # Unchanged
        assert result == {'b': 2}

    @runner.it("dissoc should handle non-existent keys gracefully")
    def test_dissoc_missing_key():
        result = wt.dissoc({'a': 1, 'b': 2}, 'c')
        assert result == {'a': 1, 'b': 2}

    @runner.it("dissoc should handle empty dict")
    def test_dissoc_empty():
        result = wt.dissoc({}, 'a')
        assert result == {}

    # ========================================================================
    # valmap
    # ========================================================================

    @runner.it("valmap should apply function to all values")
    def test_valmap_basic():
        result = wt.valmap(lambda x: x * 2, {'a': 1, 'b': 2})
        assert result == {'a': 2, 'b': 4}

    @runner.it("valmap should work with string values")
    def test_valmap_strings():
        result = wt.valmap(str.upper, {'name': 'alice', 'city': 'boston'})
        assert result == FILL_ME_IN  # {'name': 'ALICE', 'city': 'BOSTON'}

    @runner.it("valmap should not modify original dict")
    def test_valmap_immutable():
        original = {'a': 1, 'b': 2}
        result = wt.valmap(lambda x: x * 2, original)
        assert original == {'a': 1, 'b': 2}

    @runner.it("valmap should preserve keys")
    def test_valmap_preserves_keys():
        result = wt.valmap(lambda x: x + 10, {'x': 1, 'y': 2, 'z': 3})
        assert set(result.keys()) == {'x', 'y', 'z'}

    # ========================================================================
    # keymap
    # ========================================================================

    @runner.it("keymap should apply function to all keys")
    def test_keymap_basic():
        result = wt.keymap(str.upper, {'a': 1, 'b': 2})
        assert result == {'A': 1, 'B': 2}

    @runner.it("keymap should work with numeric transformations")
    def test_keymap_numeric():
        result = wt.keymap(lambda x: x * 2, {1: 'a', 2: 'b'})
        assert result == FILL_ME_IN  # {2: 'a', 4: 'b'}

    @runner.it("keymap should not modify original dict")
    def test_keymap_immutable():
        original = {'a': 1, 'b': 2}
        result = wt.keymap(str.upper, original)
        assert original == {'a': 1, 'b': 2}

    @runner.it("keymap should preserve values")
    def test_keymap_preserves_values():
        result = wt.keymap(lambda x: x + '_new', {'a': 1, 'b': 2})
        assert set(result.values()) == {1, 2}

    # ========================================================================
    # valfilter
    # ========================================================================

    @runner.it("valfilter should keep only values that pass predicate")
    def test_valfilter_basic():
        result = wt.valfilter(lambda x: x > 2, {'a': 1, 'b': 3, 'c': 2, 'd': 4})
        assert result == {'b': 3, 'd': 4}

    @runner.it("valfilter should work with modulo")
    def test_valfilter_modulo():
        result = wt.valfilter(lambda x: x % 2 == 0, {'a': 1, 'b': 2, 'c': 3})
        assert result == FILL_ME_IN  # {'b': 2}

    @runner.it("valfilter should not modify original dict")
    def test_valfilter_immutable():
        original = {'a': 1, 'b': 2, 'c': 3}
        result = wt.valfilter(lambda x: x > 1, original)
        assert original == {'a': 1, 'b': 2, 'c': 3}

    @runner.it("valfilter should handle empty results")
    def test_valfilter_empty_result():
        result = wt.valfilter(lambda x: x > 100, {'a': 1, 'b': 2})
        assert result == {}

    # ========================================================================
    # get_in
    # ========================================================================

    @runner.it("get_in should retrieve nested values")
    def test_get_in_basic():
        data = {'a': {'b': {'c': 1}}}
        result = wt.get_in(['a', 'b', 'c'], data)
        assert result == 1

    @runner.it("get_in should work with multiple levels")
    def test_get_in_deep():
        data = {'x': {'y': {'z': {'w': 42}}}}
        result = wt.get_in(['x', 'y', 'z', 'w'], data)
        assert result == FILL_ME_IN  # 42

    @runner.it("get_in should return default for missing paths")
    def test_get_in_default():
        data = {'a': {'b': 1}}
        result = wt.get_in(['a', 'x'], data, default='missing')
        assert result == 'missing'

    @runner.it("get_in should return default for partially missing paths")
    def test_get_in_partial_missing():
        data = {'a': {'b': 1}}
        result = wt.get_in(['a', 'b', 'c'], data, default=None)
        assert result is None

    @runner.it("get_in should work with empty path")
    def test_get_in_empty_path():
        data = {'a': 1}
        result = wt.get_in([], data, default='empty')
        # Empty path should return the data itself or default
        assert result == data or result == 'empty'

    # ========================================================================
    # update_in
    # ========================================================================

    @runner.it("update_in should update nested values")
    def test_update_in_basic():
        data = {'a': {'b': {'c': 1}}}
        result = wt.update_in(data, ['a', 'b', 'c'], lambda x: x + 10)
        assert result == {'a': {'b': {'c': 11}}}

    @runner.it("update_in should not modify original dict")
    def test_update_in_immutable():
        data = {'a': {'b': {'c': 1}}}
        result = wt.update_in(data, ['a', 'b', 'c'], lambda x: x + 10)
        assert data == {'a': {'b': {'c': 1}}}  # Original unchanged
        assert result == {'a': {'b': {'c': 11}}}

    @runner.it("update_in should work with multiple levels")
    def test_update_in_deep():
        data = {'x': {'y': {'z': 5}}}
        result = wt.update_in(data, ['x', 'y', 'z'], lambda x: x * 2)
        assert result == FILL_ME_IN  # {'x': {'y': {'z': 10}}}

    @runner.it("update_in should preserve other keys")
    def test_update_in_preserves():
        data = {'a': {'b': 1, 'c': 2}, 'd': 3}
        result = wt.update_in(data, ['a', 'b'], lambda x: x + 10)
        assert result['a']['c'] == 2
        assert result['d'] == 3
        assert result['a']['b'] == 11


# This allows the test file to be run standalone for debugging
if __name__ == "__main__":
    runner.run()
    runner._print_results()
