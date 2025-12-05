"""
Part II Tests: Sequence Manipulation - Working with Sequences

These tests cover functions that work with sequences and return concrete lists.
"""

from tests.test_framework import TestRunner, get_runner, create_runner
import sys

# Import the module students will implement
try:
    from src import whytoolz_part2 as wt
except ImportError:
    from types import ModuleType
    wt = ModuleType('whytoolz_part2')
    sys.modules['whytoolz_part2'] = wt

# Get the global test runner
runner = get_runner() or create_runner()



@runner.describe("Part II: Sequence Manipulation")
def test_part2():
    """Tests for sequence manipulation functions"""

    @runner.subsuite("islice")
    def test_islice():
        # ========================================================================
        # islice
        # ========================================================================

        @runner.it("islice should return a list")
        def test_islice_returns_list():
            result = wt.islice([1, 2, 3, 4, 5], 3)
            assert isinstance(result, list), \
                "islice should return a list"

        @runner.it("islice with single argument should return first n elements")
        def test_islice_single_arg():
            result = wt.islice([1, 2, 3, 4, 5], 3)
            assert result == [1, 2, 3]

        @runner.it("islice with two arguments should return slice [start:stop]")
        def test_islice_two_args():
            result = list(wt.islice([1, 2, 3, 4, 5], 1, 4))
            assert result == [2, 3, 4]

        @runner.it("islice with three arguments should return slice with step")
        def test_islice_three_args():
            result = list(wt.islice([1, 2, 3, 4, 5], 0, 5, 2))
            assert result == [1, 3, 5]

        @runner.it("islice should work with strings")
        def test_islice_string():
            result = list(wt.islice('hello', 2))
            assert result == ['h', 'e']

        @runner.it("islice should handle n larger than sequence length")
        def test_islice_oversized():
            result = list(wt.islice([1, 2, 3], 10))
            assert result == [1, 2, 3]

        @runner.it("islice should handle n = 0")
        def test_islice_zero():
            result = list(wt.islice([1, 2, 3], 0))
            assert result == []

        @runner.it("islice with start >= length should return empty")
        def test_islice_start_beyond():
            result = list(wt.islice([1, 2, 3], 10, 20))
            assert result == []

        @runner.it("islice should work with step = 1 (default)")
        def test_islice_step_one():
            result = list(wt.islice([1, 2, 3, 4, 5], 1, 4, 1))
            assert result == [2, 3, 4]

    @runner.subsuite("drop")
    def test_drop():
        # ========================================================================
        # drop
        # ========================================================================

        @runner.it("drop should return a list")
        def test_drop_returns_list():
            result = wt.drop(2, [1, 2, 3, 4, 5])
            assert isinstance(result, list), \
                "drop should return a list"

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
            assert result == []

        @runner.it("drop should handle n = 0")
        def test_drop_zero():
            result = list(wt.drop(0, [1, 2, 3]))
            assert result == [1, 2, 3]

    @runner.subsuite("tail")
    def test_tail():
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
            assert result == ['l', 'l', 'o']

        @runner.it("tail should handle n larger than sequence length")
        def test_tail_oversized():
            result = wt.tail(10, [1, 2, 3])
            assert result == [1, 2, 3]

        @runner.it("tail should handle n = 0")
        def test_tail_zero():
            result = wt.tail(0, [1, 2, 3])
            assert result == []

    @runner.subsuite("concat")
    def test_concat():
        # ========================================================================
        # concat
        # ========================================================================

        @runner.it("concat should return a list")
        def test_concat_returns_list():
            result = wt.concat([[1, 2], [3, 4]])
            assert isinstance(result, list), \
                "concat should return a list"

        @runner.it("concat should flatten one level of nesting")
        def test_concat_basic():
            result = list(wt.concat([[1, 2], [3, 4], [5]]))
            assert result == [1, 2, 3, 4, 5]

        @runner.it("concat should work with strings")
        def test_concat_strings():
            result = list(wt.concat(['ab', 'cd', 'ef']))
            assert result == ['a', 'b', 'c', 'd', 'e', 'f']

        @runner.it("concat should handle empty sequences")
        def test_concat_empty():
            result = list(wt.concat([[], [1, 2], [], [3]]))
            assert result == [1, 2, 3]

        @runner.it("concat should only flatten one level")
        def test_concat_nested():
            result = list(wt.concat([[1, [2, 3]], [4, [5]]]))
            assert result == [1, [2, 3], 4, [5]]

    @runner.subsuite("unique")
    def test_unique():
        # ========================================================================
        # unique
        # ========================================================================

        @runner.it("unique should return a list")
        def test_unique_returns_list():
            result = wt.unique([1, 2, 3])
            assert isinstance(result, list), \
                "unique should return a list"

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
            assert result == [1, 2, 3, 4]

        @runner.it("unique should handle empty sequences")
        def test_unique_empty():
            result = list(wt.unique([]))
            assert result == []

    @runner.subsuite("partition")
    def test_partition():
        # ========================================================================
        # partition
        # ========================================================================

        @runner.it("partition should return a list of tuples")
        def test_partition_returns_list():
            result = wt.partition(2, [1, 2, 3, 4])
            assert isinstance(result, list), \
                "partition should return a list"

        @runner.it("partition should split sequence into chunks of size n")
        def test_partition_basic():
            result = list(wt.partition(2, [1, 2, 3, 4, 5, 6]))
            assert result == [(1, 2), (3, 4), (5, 6)]

        @runner.it("partition should handle remainder (incomplete final chunk)")
        def test_partition_remainder():
            result = list(wt.partition(2, [1, 2, 3, 4, 5]))
            assert result == [(1, 2), (3, 4), (5,)]

        @runner.it("partition should work with strings")
        def test_partition_string():
            result = list(wt.partition(3, 'hello'))
            assert result == [('h', 'e', 'l'), ('l', 'o')]

        @runner.it("partition should work with n = 1")
        def test_partition_one():
            result = list(wt.partition(1, [1, 2, 3]))
            assert result == [(1,), (2,), (3,)]

    @runner.subsuite("interleave")
    def test_interleave():
        # ========================================================================
        # interleave
        # ========================================================================

        @runner.it("interleave should return a list")
        def test_interleave_returns_list():
            result = wt.interleave([[1, 2], [3, 4]])
            assert isinstance(result, list), \
                "interleave should return a list"

        @runner.it("interleave should alternate elements from sequences")
        def test_interleave_basic():
            result = list(wt.interleave([[1, 2], [3, 4], [5, 6]]))
            assert result == [1, 3, 5, 2, 4, 6]

        @runner.it("interleave should work with strings")
        def test_interleave_strings():
            result = list(wt.interleave(['ab', 'cd']))
            assert result == ['a', 'c', 'b', 'd']

        @runner.it("interleave should handle sequences of different lengths")
        def test_interleave_uneven():
            result = list(wt.interleave([[1, 2, 3], [4, 5], [6]]))
            assert result == [1, 4, 6, 2, 5, 3]

        @runner.it("interleave should handle empty sequences")
        def test_interleave_empty():
            result = list(wt.interleave([[], [1, 2], []]))
            assert result == [1, 2]

    @runner.subsuite("pluck")
    def test_pluck():
        # ========================================================================
        # pluck
        # ========================================================================

        @runner.it("pluck should return a list")
        def test_pluck_returns_list():
            result = wt.pluck('name', [{'name': 'Alice'}])
            assert isinstance(result, list), \
                "pluck should return a list"

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
            assert result == [2, 4]

        @runner.it("pluck should work with integer keys")
        def test_pluck_int_keys():
            data = [{0: 'a', 1: 'b'}, {0: 'c', 1: 'd'}]
            result = list(wt.pluck(0, data))
            assert result == ['a', 'c']

    @runner.subsuite("accumulate")
    def test_accumulate():
        # ========================================================================
        # accumulate
        # ========================================================================

        @runner.it("accumulate should return a list")
        def test_accumulate_returns_list():
            def add(x, y):
                return x + y
            result = wt.accumulate(add, [1, 2, 3])
            assert isinstance(result, list), \
                "accumulate should return a list"

        @runner.it("accumulate should return running sum with initial value")
        def test_accumulate_sum():
            def add(x, y):
                return x + y
            result = list(wt.accumulate(add, [1, 2, 3, 4], 0))
            assert result == [0, 1, 3, 6, 10]

        @runner.it("accumulate should work with multiplication")
        def test_accumulate_product():
            def multiply(x, y):
                return x * y
            result = list(wt.accumulate(multiply, [1, 2, 3, 4], 1))
            assert result == [1, 1, 2, 6, 24]

        @runner.it("accumulate should work without initial value")
        def test_accumulate_no_init():
            def add(x, y):
                return x + y
            result = list(wt.accumulate(add, [1, 2, 3, 4]))
            assert result == [1, 3, 6, 10]

        @runner.it("accumulate should handle empty sequence with initial")
        def test_accumulate_empty_with_init():
            def add(x, y):
                return x + y
            result = list(wt.accumulate(add, [], 10))
            assert result == [10]

    @runner.subsuite("sliding_window")
    def test_sliding_window():
        # ========================================================================
        # sliding_window
        # ========================================================================

        @runner.it("sliding_window should return a list of tuples")
        def test_sliding_window_returns_list():
            result = wt.sliding_window(2, [1, 2, 3])
            assert isinstance(result, list), \
                "sliding_window should return a list"

        @runner.it("sliding_window should create overlapping windows")
        def test_sliding_window_basic():
            result = list(wt.sliding_window(2, [1, 2, 3, 4]))
            assert result == [(1, 2), (2, 3), (3, 4)]

        @runner.it("sliding_window should work with window size 3")
        def test_sliding_window_three():
            result = list(wt.sliding_window(3, 'hello'))
            assert result == [('h', 'e', 'l'), ('e', 'l', 'l'), ('l', 'l', 'o')]

        @runner.it("sliding_window should handle sequence shorter than window")
        def test_sliding_window_short():
            result = list(wt.sliding_window(5, [1, 2, 3]))
            assert result == []

        @runner.it("sliding_window should work with window size 1")
        def test_sliding_window_one():
            result = list(wt.sliding_window(1, [1, 2, 3]))
            assert result == [(1,), (2,), (3,)]

    @runner.subsuite("take_nth")
    def test_take_nth():
        # ========================================================================
        # take_nth
        # ========================================================================

        @runner.it("take_nth should return a list")
        def test_take_nth_returns_list():
            result = wt.take_nth(2, [1, 2, 3, 4, 5])
            assert isinstance(result, list), \
                "take_nth should return a list"

        @runner.it("take_nth should return every nth element")
        def test_take_nth_basic():
            result = list(wt.take_nth(2, [0, 1, 2, 3, 4, 5, 6]))
            assert result == [0, 2, 4, 6]

        @runner.it("take_nth should work with n = 3")
        def test_take_nth_three():
            result = list(wt.take_nth(3, 'hello world'))
            assert result == ['h', 'l', 'o', 'l']

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