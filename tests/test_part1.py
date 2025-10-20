"""
Part I Tests: Foundation - Working with Concrete Data Structures

These tests cover basic functions that return concrete data (lists, dicts, values).
No generators yet - we'll learn those in Part II!
"""

from tests.test_framework import TestRunner

# Import the module students will implement
try:
    from src import whytoolz as wt
except ImportError:
    # If module doesn't exist, create a dummy for testing
    import sys
    from types import ModuleType
    wt = ModuleType('whytoolz')
    sys.modules['whytoolz'] = wt

# Get the global test runner
from tests.test_framework import get_runner, create_runner
runner = get_runner() or create_runner()

# Special value for fill-in-the-blank tests
FILL_ME_IN = "Fill this value in"


@runner.describe("Part I: Foundation Functions")
def test_part1():
    """Tests for basic non-generator functions"""

    # ========================================================================
    # identity
    # ========================================================================

    @runner.it("identity should return whatever value is passed into it")
    def test_identity_returns_input():
        assert wt.identity(1) == 1
        assert wt.identity('string') == 'string'
        assert wt.identity(False) is False
        assert wt.identity(None) is None

    @runner.it("identity should return the same object (not a copy)")
    def test_identity_same_object():
        unique_list = [1, 2, 3]
        unique_dict = {'key': 'value'}
        assert wt.identity(unique_list) is unique_list
        assert wt.identity(unique_dict) is unique_dict

    # ========================================================================
    # first
    # ========================================================================

    @runner.it("first should be able to pull out the first element of a list")
    def test_first_list():
        assert wt.first([1, 2, 3]) == FILL_ME_IN

    @runner.it("first should work on strings")
    def test_first_string():
        assert wt.first('hello') == 'h'
        assert wt.first('a') == 'a'

    @runner.it("first should work on tuples")
    def test_first_tuple():
        assert wt.first((10, 20, 30)) == 10

    @runner.it("first should work on any iterable")
    def test_first_iterable():
        assert wt.first(range(5, 10)) == 5
        assert wt.first({'a': 1, 'b': 2}) in ['a', 'b']  # dict keys

    # ========================================================================
    # second
    # ========================================================================

    @runner.it("second should pull the second element from a list")
    def test_second_list():
        assert wt.second([1, 2, 3]) == 2
        assert wt.second([10, 20]) == 20

    @runner.it("second should work on strings")
    def test_second_string():
        assert wt.second('hello') == FILL_ME_IN

    @runner.it("second should work on any iterable")
    def test_second_iterable():
        assert wt.second(range(5, 10)) == 6

    # ========================================================================
    # last
    # ========================================================================

    @runner.it("last should pull the last element from a list")
    def test_last_list():
        assert wt.last([1, 2, 3]) == 3
        assert wt.last([5]) == 5

    @runner.it("last should work on strings")
    def test_last_string():
        assert wt.last('hello') == 'o'
        assert wt.last('a') == FILL_ME_IN

    @runner.it("last should work on tuples")
    def test_last_tuple():
        assert wt.last((10, 20, 30)) == 30

    @runner.it("last should work on iterables (even if only iterable once)")
    def test_last_iterable():
        # This tests that last() can handle generators
        assert wt.last(x for x in range(5)) == 4

    # ========================================================================
    # nth
    # ========================================================================

    @runner.it("nth should return the element at the given index")
    def test_nth_basic():
        assert wt.nth(0, [1, 2, 3, 4, 5]) == 1
        assert wt.nth(2, [1, 2, 3, 4, 5]) == FILL_ME_IN
        assert wt.nth(4, [1, 2, 3, 4, 5]) == 5

    @runner.it("nth should work on strings")
    def test_nth_string():
        assert wt.nth(0, 'hello') == 'h'
        assert wt.nth(4, 'hello') == 'o'

    @runner.it("nth should work with iterables")
    def test_nth_iterable():
        assert wt.nth(3, range(10)) == 3

    # ========================================================================
    # count
    # ========================================================================

    @runner.it("count should determine the number of items in a list")
    def test_count_list():
        assert wt.count([1, 2, 3]) == 3
        assert wt.count([]) == 0
        assert wt.count([1, 2, 3, 4, 5]) == FILL_ME_IN

    @runner.it("count should work on strings")
    def test_count_string():
        assert wt.count('hello') == 5
        assert wt.count('') == 0

    @runner.it("count should work on any iterable, including generators")
    def test_count_iterable():
        assert wt.count(range(10)) == 10
        assert wt.count(x for x in range(5)) == 5

    # ========================================================================
    # frequencies
    # ========================================================================

    @runner.it("frequencies should count occurrences of each element")
    def test_frequencies_basic():
        result = wt.frequencies(['a', 'b', 'a', 'c', 'b', 'a'])
        assert result == {'a': 3, 'b': 2, 'c': 1}

    @runner.it("frequencies should work with numbers")
    def test_frequencies_numbers():
        result = wt.frequencies([1, 1, 2, 3, 2, 1])
        assert result == FILL_ME_IN  # Student fills in: {1: 3, 2: 2, 3: 1}

    @runner.it("frequencies should work with strings (counts characters)")
    def test_frequencies_string():
        result = wt.frequencies('hello')
        assert result['l'] == 2
        assert result['h'] == 1
        assert result['e'] == 1
        assert result['o'] == 1

    @runner.it("frequencies should handle empty sequences")
    def test_frequencies_empty():
        assert wt.frequencies([]) == {}
        assert wt.frequencies('') == {}

    # ========================================================================
    # groupby
    # ========================================================================

    @runner.it("groupby should group elements by a key function")
    def test_groupby_basic():
        result = wt.groupby(len, ['a', 'bb', 'ccc', 'dd', 'e'])
        assert result == {1: ['a', 'e'], 2: ['bb', 'dd'], 3: ['ccc']}

    @runner.it("groupby should work with numeric keys")
    def test_groupby_numeric():
        result = wt.groupby(lambda x: x % 2, [1, 2, 3, 4, 5, 6])
        assert result == FILL_ME_IN  # {1: [1, 3, 5], 0: [2, 4, 6]}

    @runner.it("groupby should work with property access")
    def test_groupby_property():
        data = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25},
            {'name': 'Charlie', 'age': 30}
        ]
        result = wt.groupby(lambda x: x['age'], data)
        assert len(result[30]) == 2
        assert len(result[25]) == 1

    @runner.it("groupby should preserve order within groups")
    def test_groupby_order():
        result = wt.groupby(lambda x: x > 0, [1, -2, 3, -4, 5])
        assert result[True] == [1, 3, 5]
        assert result[False] == [-2, -4]

    # ========================================================================
    # cons
    # ========================================================================

    @runner.it("cons should prepend an element to a list")
    def test_cons_list():
        assert wt.cons(1, [2, 3, 4]) == [1, 2, 3, 4]
        assert wt.cons(0, [1, 2]) == [0, 1, 2]

    @runner.it("cons should work with strings")
    def test_cons_string():
        result = wt.cons('a', 'bcd')
        assert result == FILL_ME_IN  # ['a', 'b', 'c', 'd']

    @runner.it("cons should work with any iterable")
    def test_cons_iterable():
        assert wt.cons(1, range(2, 5)) == [1, 2, 3, 4]

    @runner.it("cons should return a new list (not modify original)")
    def test_cons_immutable():
        original = [2, 3, 4]
        result = wt.cons(1, original)
        assert original == [2, 3, 4]  # Unchanged
        assert result == [1, 2, 3, 4]
        assert result is not original

    @runner.it("cons should work with empty sequences")
    def test_cons_empty():
        assert wt.cons(1, []) == [1]

    # ========================================================================
    # merge
    # ========================================================================

    @runner.it("merge should combine multiple dictionaries")
    def test_merge_basic():
        result = wt.merge({'a': 1}, {'b': 2}, {'c': 3})
        assert result == {'a': 1, 'b': 2, 'c': 3}

    @runner.it("merge should handle later dictionaries overriding earlier ones")
    def test_merge_override():
        result = wt.merge({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
        assert result == FILL_ME_IN  # {'a': 1, 'b': 3, 'c': 4}

    @runner.it("merge should handle multiple overrides (last wins)")
    def test_merge_multiple_override():
        result = wt.merge({'x': 1}, {'x': 2}, {'x': 3})
        assert result['x'] == 3

    @runner.it("merge should return a new dictionary (not modify originals)")
    def test_merge_immutable():
        dict1 = {'a': 1}
        dict2 = {'b': 2}
        result = wt.merge(dict1, dict2)
        assert dict1 == {'a': 1}  # Unchanged
        assert dict2 == {'b': 2}  # Unchanged
        assert result == {'a': 1, 'b': 2}

    @runner.it("merge should handle empty dictionaries")
    def test_merge_empty():
        assert wt.merge({}, {'a': 1}) == {'a': 1}
        assert wt.merge({'a': 1}, {}) == {'a': 1}
        assert wt.merge() == {}

    @runner.it("merge should handle a single dictionary")
    def test_merge_single():
        result = wt.merge({'a': 1, 'b': 2})
        assert result == {'a': 1, 'b': 2}


# This allows the test file to be run standalone for debugging
if __name__ == "__main__":
    runner.run()
    runner._print_results()
