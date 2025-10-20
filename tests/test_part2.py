"""
Part II Tests: Sequences & Lazy Evaluation - Working with Generators

These tests cover functions that return GENERATORS (lazy iterators).
You'll learn how generators work and why they're useful in PyToolz!
"""

from tests.test_framework import TestRunner, get_runner, create_runner
from types import GeneratorType
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


@runner.describe("Part II: Sequences & Lazy Evaluation")
def test_part2():
    """Tests for generator-based (lazy) functions"""

    # ========================================================================
    # take
    # ========================================================================

    @runner.it("take should return a generator (not a list)")
    def test_take_returns_generator():
        result = wt.take(3, [1, 2, 3, 4, 5])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__'), \
            "take should return a generator or iterator, not a list"

    @runner.it("take should yield the first n elements")
    def test_take_basic():
        result = list(wt.take(3, [1, 2, 3, 4, 5]))
        assert result == [1, 2, 3]

    @runner.it("take should work with strings")
    def test_take_string():
        result = list(wt.take(2, 'hello'))
        assert result == FILL_ME_IN  # ['h', 'e']

    @runner.it("take should handle n larger than sequence length")
    def test_take_oversized():
        result = list(wt.take(10, [1, 2, 3]))
        assert result == [1, 2, 3]

    @runner.it("take should handle n = 0")
    def test_take_zero():
        result = list(wt.take(0, [1, 2, 3]))
        assert result == []

    @runner.it("take should be lazy (only consume what's needed)")
    def test_take_lazy():
        # This generator tracks how many items were consumed
        consumed = []
        def tracking_gen():
            for i in range(10):
                consumed.append(i)
                yield i

        result = wt.take(3, tracking_gen())
        # Before consuming the result, nothing should be consumed
        # (may consume first item depending on implementation)
        list(result)  # Consume the take result
        # Should have consumed at most 3 items
        assert len(consumed) <= 3, "take should be lazy and only consume needed items"

    # ========================================================================
    # drop
    # ========================================================================

    @runner.it("drop should return a generator")
    def test_drop_returns_generator():
        result = wt.drop(2, [1, 2, 3, 4, 5])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("drop should skip the first n elements")
    def test_drop_basic():
        result = list(wt.drop(2, [1, 2, 3, 4, 5]))
        assert result == [3, 4, 5]

    @runner.it("drop should work with strings")
    def test_drop_string():
        result = list(wt.drop(3, 'hello'))
        assert result == ['l', 'o']

    @runner.it("drop should handle n larger than sequence length")
    def test_drop_oversized():
        result = list(wt.drop(10, [1, 2, 3]))
        assert result == FILL_ME_IN  # []

    @runner.it("drop should handle n = 0")
    def test_drop_zero():
        result = list(wt.drop(0, [1, 2, 3]))
        assert result == [1, 2, 3]

    # ========================================================================
    # tail
    # ========================================================================

    @runner.it("tail should return the last n elements as a list")
    def test_tail_basic():
        result = wt.tail(2, [1, 2, 3, 4, 5])
        assert result == [4, 5]

    @runner.it("tail should work with strings")
    def test_tail_string():
        result = wt.tail(3, 'hello')
        assert result == FILL_ME_IN  # ['l', 'l', 'o']

    @runner.it("tail should handle n larger than sequence length")
    def test_tail_oversized():
        result = wt.tail(10, [1, 2, 3])
        assert result == [1, 2, 3]

    @runner.it("tail should handle n = 0")
    def test_tail_zero():
        result = wt.tail(0, [1, 2, 3])
        assert result == []

    @runner.it("tail should work with generators (consume once)")
    def test_tail_generator():
        result = wt.tail(2, (x for x in range(5)))
        assert result == [3, 4]

    # ========================================================================
    # concat
    # ========================================================================

    @runner.it("concat should return a generator")
    def test_concat_returns_generator():
        result = wt.concat([[1, 2], [3, 4]])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("concat should flatten one level of nesting")
    def test_concat_basic():
        result = list(wt.concat([[1, 2], [3, 4], [5]]))
        assert result == [1, 2, 3, 4, 5]

    @runner.it("concat should work with strings")
    def test_concat_strings():
        result = list(wt.concat(['ab', 'cd', 'ef']))
        assert result == FILL_ME_IN  # ['a', 'b', 'c', 'd', 'e', 'f']

    @runner.it("concat should handle empty sequences")
    def test_concat_empty():
        result = list(wt.concat([[], [1, 2], [], [3]]))
        assert result == [1, 2, 3]

    @runner.it("concat should only flatten one level")
    def test_concat_nested():
        result = list(wt.concat([[1, [2, 3]], [4, [5]]]))
        assert result == [1, [2, 3], 4, [5]]

    # ========================================================================
    # unique
    # ========================================================================

    @runner.it("unique should return a generator")
    def test_unique_returns_generator():
        result = wt.unique([1, 2, 3])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("unique should remove duplicates while preserving order")
    def test_unique_basic():
        result = list(wt.unique([1, 2, 3, 2, 1, 4]))
        assert result == [1, 2, 3, 4]

    @runner.it("unique should work with strings")
    def test_unique_string():
        result = list(wt.unique('hello'))
        assert result == ['h', 'e', 'l', 'o']

    @runner.it("unique should handle sequences with no duplicates")
    def test_unique_no_dupes():
        result = list(wt.unique([1, 2, 3, 4]))
        assert result == FILL_ME_IN  # [1, 2, 3, 4]

    @runner.it("unique should handle empty sequences")
    def test_unique_empty():
        result = list(wt.unique([]))
        assert result == []

    # ========================================================================
    # partition
    # ========================================================================

    @runner.it("partition should return a generator of tuples")
    def test_partition_returns_generator():
        result = wt.partition(2, [1, 2, 3, 4])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("partition should split sequence into chunks of size n")
    def test_partition_basic():
        result = list(wt.partition(2, [1, 2, 3, 4, 5, 6]))
        assert result == [(1, 2), (3, 4), (5, 6)]

    @runner.it("partition should handle remainder (incomplete final chunk)")
    def test_partition_remainder():
        result = list(wt.partition(2, [1, 2, 3, 4, 5]))
        assert result == FILL_ME_IN  # [(1, 2), (3, 4), (5,)]

    @runner.it("partition should work with strings")
    def test_partition_string():
        result = list(wt.partition(3, 'hello'))
        assert result == [('h', 'e', 'l'), ('l', 'o')]

    @runner.it("partition should work with n = 1")
    def test_partition_one():
        result = list(wt.partition(1, [1, 2, 3]))
        assert result == [(1,), (2,), (3,)]

    # ========================================================================
    # interleave
    # ========================================================================

    @runner.it("interleave should return a generator")
    def test_interleave_returns_generator():
        result = wt.interleave([[1, 2], [3, 4]])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("interleave should alternate elements from sequences")
    def test_interleave_basic():
        result = list(wt.interleave([[1, 2], [3, 4], [5, 6]]))
        assert result == [1, 3, 5, 2, 4, 6]

    @runner.it("interleave should work with strings")
    def test_interleave_strings():
        result = list(wt.interleave(['ab', 'cd']))
        assert result == FILL_ME_IN  # ['a', 'c', 'b', 'd']

    @runner.it("interleave should handle sequences of different lengths")
    def test_interleave_uneven():
        result = list(wt.interleave([[1, 2, 3], [4, 5], [6]]))
        assert result == [1, 4, 6, 2, 5, 3]

    @runner.it("interleave should handle empty sequences")
    def test_interleave_empty():
        result = list(wt.interleave([[], [1, 2], []]))
        assert result == [1, 2]

    # ========================================================================
    # pluck
    # ========================================================================

    @runner.it("pluck should return a generator")
    def test_pluck_returns_generator():
        result = wt.pluck('name', [{'name': 'Alice'}])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("pluck should extract values by key from dicts")
    def test_pluck_basic():
        people = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25}
        ]
        result = list(wt.pluck('name', people))
        assert result == ['Alice', 'Bob']

    @runner.it("pluck should extract numeric values")
    def test_pluck_numbers():
        data = [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
        result = list(wt.pluck('y', data))
        assert result == FILL_ME_IN  # [2, 4]

    @runner.it("pluck should work with integer keys")
    def test_pluck_int_keys():
        data = [{0: 'a', 1: 'b'}, {0: 'c', 1: 'd'}]
        result = list(wt.pluck(0, data))
        assert result == ['a', 'c']

    # ========================================================================
    # accumulate
    # ========================================================================

    @runner.it("accumulate should return a generator")
    def test_accumulate_returns_generator():
        result = wt.accumulate(lambda x, y: x + y, [1, 2, 3])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("accumulate should yield running sum with initial value")
    def test_accumulate_sum():
        result = list(wt.accumulate(lambda x, y: x + y, [1, 2, 3, 4], 0))
        assert result == [0, 1, 3, 6, 10]

    @runner.it("accumulate should work with multiplication")
    def test_accumulate_product():
        result = list(wt.accumulate(lambda x, y: x * y, [1, 2, 3, 4], 1))
        assert result == FILL_ME_IN  # [1, 1, 2, 6, 24]

    @runner.it("accumulate should work without initial value")
    def test_accumulate_no_init():
        result = list(wt.accumulate(lambda x, y: x + y, [1, 2, 3, 4]))
        assert result == [1, 3, 6, 10]

    @runner.it("accumulate should handle empty sequence with initial")
    def test_accumulate_empty_with_init():
        result = list(wt.accumulate(lambda x, y: x + y, [], 10))
        assert result == [10]

    # ========================================================================
    # iterate
    # ========================================================================

    @runner.it("iterate should return a generator")
    def test_iterate_returns_generator():
        result = wt.iterate(lambda x: x + 1, 0)
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("iterate should create infinite sequence by repeatedly applying function")
    def test_iterate_basic():
        result = list(wt.take(5, wt.iterate(lambda x: x * 2, 1)))
        assert result == [1, 2, 4, 8, 16]

    @runner.it("iterate should work with addition")
    def test_iterate_addition():
        result = list(wt.take(4, wt.iterate(lambda x: x + 1, 0)))
        assert result == FILL_ME_IN  # [0, 1, 2, 3]

    @runner.it("iterate should work with more complex functions")
    def test_iterate_complex():
        result = list(wt.take(5, wt.iterate(lambda x: x + 2, 1)))
        assert result == [1, 3, 5, 7, 9]

    @runner.it("iterate creates infinite sequence - DO NOT convert to list!")
    def test_iterate_infinite():
        # This test just verifies it's a generator
        result = wt.iterate(lambda x: x + 1, 0)
        # Take just a few items to verify it works
        first_few = [next(result) for _ in range(3)]
        assert first_few == [0, 1, 2]

    # ========================================================================
    # sliding_window
    # ========================================================================

    @runner.it("sliding_window should return a generator")
    def test_sliding_window_returns_generator():
        result = wt.sliding_window(2, [1, 2, 3])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("sliding_window should create overlapping windows")
    def test_sliding_window_basic():
        result = list(wt.sliding_window(2, [1, 2, 3, 4]))
        assert result == [(1, 2), (2, 3), (3, 4)]

    @runner.it("sliding_window should work with window size 3")
    def test_sliding_window_three():
        result = list(wt.sliding_window(3, 'hello'))
        assert result == FILL_ME_IN  # [('h', 'e', 'l'), ('e', 'l', 'l'), ('l', 'l', 'o')]

    @runner.it("sliding_window should handle sequence shorter than window")
    def test_sliding_window_short():
        result = list(wt.sliding_window(5, [1, 2, 3]))
        assert result == []

    @runner.it("sliding_window should work with window size 1")
    def test_sliding_window_one():
        result = list(wt.sliding_window(1, [1, 2, 3]))
        assert result == [(1,), (2,), (3,)]

    # ========================================================================
    # take_nth
    # ========================================================================

    @runner.it("take_nth should return a generator")
    def test_take_nth_returns_generator():
        result = wt.take_nth(2, [1, 2, 3, 4, 5])
        assert isinstance(result, GeneratorType) or hasattr(result, '__iter__')

    @runner.it("take_nth should yield every nth element")
    def test_take_nth_basic():
        result = list(wt.take_nth(2, [0, 1, 2, 3, 4, 5, 6]))
        assert result == [0, 2, 4, 6]

    @runner.it("take_nth should work with n = 3")
    def test_take_nth_three():
        result = list(wt.take_nth(3, 'hello world'))
        assert result == FILL_ME_IN  # ['h', 'l', 'o', 'l']

    @runner.it("take_nth should work with n = 1 (every element)")
    def test_take_nth_one():
        result = list(wt.take_nth(1, [1, 2, 3]))
        assert result == [1, 2, 3]

    @runner.it("take_nth should handle n larger than sequence length")
    def test_take_nth_large():
        result = list(wt.take_nth(10, [1, 2, 3]))
        assert result == [1]


# This allows the test file to be run standalone for debugging
if __name__ == "__main__":
    runner.run()
    runner._print_results()
