"""
Part IV Tests: Advanced - Optional Challenge Functions

These are more complex functions for students who finish early
or want extra challenges. Good luck!
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


@runner.describe("Part IV: Advanced (Optional)")
def test_advanced():
    """Tests for advanced challenge functions"""

    # ========================================================================
    # topk
    # ========================================================================

    @runner.it("topk should return the k largest elements")
    def test_topk_basic():
        result = wt.topk(3, [1, 5, 3, 9, 2, 7])
        assert result == [9, 7, 5]

    @runner.it("topk should work with k = 1")
    def test_topk_one():
        result = wt.topk(1, [3, 1, 4, 1, 5])
        assert result == [5]

    @runner.it("topk should work with strings (by character)")
    def test_topk_strings():
        result = wt.topk(2, 'hello world')
        assert result == FILL_ME_IN  # ['w', 'r'] (or similar, depends on sorting)

    @runner.it("topk should handle k larger than sequence length")
    def test_topk_oversized():
        result = wt.topk(10, [1, 2, 3])
        assert len(result) == 3
        assert result[0] == 3  # Largest first

    @runner.it("topk should handle duplicates")
    def test_topk_duplicates():
        result = wt.topk(3, [5, 5, 3, 3, 1])
        assert len(result) == 3
        assert result[0] == 5 or result[0] == 5  # Top values are 5s and 3s

    @runner.it("topk should return results in descending order")
    def test_topk_descending():
        result = wt.topk(4, [1, 2, 3, 4, 5])
        assert result == [5, 4, 3, 2]

    # ========================================================================
    # reduceby
    # ========================================================================

    @runner.it("reduceby should group and reduce simultaneously")
    def test_reduceby_basic():
        data = [('a', 1), ('b', 2), ('a', 3), ('b', 4)]
        result = wt.reduceby(
            lambda x: x[0],  # Key function: first element
            lambda acc, x: acc + x[1],  # Reduction: sum second elements
            data,
            0  # Initial value
        )
        assert result == {'a': 4, 'b': 6}  # a: 1+3=4, b: 2+4=6

    @runner.it("reduceby should work with string keys")
    def test_reduceby_strings():
        data = ['apple', 'apricot', 'banana', 'blueberry', 'cherry']
        result = wt.reduceby(
            lambda x: x[0],  # Group by first letter
            lambda acc, x: acc + 1,  # Count
            data,
            0
        )
        assert result == FILL_ME_IN  # {'a': 2, 'b': 2, 'c': 1}

    @runner.it("reduceby should work with multiplication")
    def test_reduceby_product():
        data = [('x', 2), ('y', 3), ('x', 4), ('y', 5)]
        result = wt.reduceby(
            lambda x: x[0],
            lambda acc, x: acc * x[1],
            data,
            1  # Initial: 1 for multiplication
        )
        assert result == {'x': 8, 'y': 15}  # x: 2*4=8, y: 3*5=15

    @runner.it("reduceby should handle empty sequences")
    def test_reduceby_empty():
        result = wt.reduceby(
            lambda x: x[0],
            lambda acc, x: acc + x[1],
            [],
            0
        )
        assert result == {}

    @runner.it("reduceby should work with complex aggregations")
    def test_reduceby_complex():
        # Build lists of values for each key
        data = [('a', 1), ('b', 2), ('a', 3), ('b', 4)]
        result = wt.reduceby(
            lambda x: x[0],
            lambda acc, x: acc + [x[1]],  # Accumulate into list
            data,
            []
        )
        assert result == {'a': [1, 3], 'b': [2, 4]}

    # ========================================================================
    # juxt
    # ========================================================================

    @runner.it("juxt should create function that applies multiple functions")
    def test_juxt_basic():
        f = wt.juxt(lambda x: x * 2, lambda x: x + 1, lambda x: x ** 2)
        result = f(3)
        assert result == (6, 4, 9)

    @runner.it("juxt should work with built-in functions")
    def test_juxt_builtins():
        f = wt.juxt(len, sum, max)
        result = f([1, 2, 3, 4, 5])
        assert result == FILL_ME_IN  # (5, 15, 5)

    @runner.it("juxt should return a callable")
    def test_juxt_callable():
        f = wt.juxt(lambda x: x + 1, lambda x: x * 2)
        assert callable(f)

    @runner.it("juxt should work with single function")
    def test_juxt_single():
        f = wt.juxt(lambda x: x * 2)
        result = f(5)
        assert result == (10,)  # Still returns tuple

    @runner.it("juxt should work with string operations")
    def test_juxt_strings():
        f = wt.juxt(str.upper, str.lower, len)
        result = f('Hello')
        assert result == ('HELLO', 'hello', 5)

    # ========================================================================
    # curry
    # ========================================================================

    @runner.it("curry should allow partial application")
    def test_curry_basic():
        def add(a, b, c):
            return a + b + c

        curried_add = wt.curry(add)
        result = curried_add(1)(2)(3)
        assert result == 6

    @runner.it("curry should allow calling with multiple args at once")
    def test_curry_multi_args():
        def add(a, b, c):
            return a + b + c

        curried_add = wt.curry(add)
        result = curried_add(1, 2)(3)
        assert result == 6

    @runner.it("curry should allow all args at once")
    def test_curry_all_args():
        def add(a, b, c):
            return a + b + c

        curried_add = wt.curry(add)
        result = curried_add(1, 2, 3)
        assert result == 6

    @runner.it("curry should create reusable partial functions")
    def test_curry_reusable():
        def multiply(a, b, c):
            return a * b * c

        curried = wt.curry(multiply)
        times_2 = curried(2)
        times_2_3 = times_2(3)

        assert times_2_3(4) == FILL_ME_IN  # 2 * 3 * 4 = 24
        assert times_2_3(5) == 30  # 2 * 3 * 5 = 30

    @runner.it("curry should work with two-argument functions")
    def test_curry_two_args():
        def power(base, exp):
            return base ** exp

        curried = wt.curry(power)
        square = curried(exp=2)  # Or however your curry handles kwargs
        # This test is flexible based on implementation
        result = curried(3, 2)
        assert result == 9

    @runner.it("curry should handle functions with one argument")
    def test_curry_one_arg():
        def double(x):
            return x * 2

        curried = wt.curry(double)
        result = curried(5)
        assert result == 10


# This allows the test file to be run standalone for debugging
if __name__ == "__main__":
    runner.run()
    runner._print_results()
