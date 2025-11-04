"""
WhyToolz Part I: Foundation - Working with Concrete Data Structures

In this section, you'll implement basic functions that work with lists,
dictionaries, and single values. These functions return concrete data
(not generators), making them easier to understand and debug.

Focus on:
- Understanding function signatures and return types
- Working with Python's indexing and slicing
- Building dictionaries from scratch
- Recursion for nested structures

See: https://toolz.readthedocs.io/en/latest/api.html#itertoolz
"""


def identity(x):
    """
    Return the input unchanged.

    While this seems trivial, identity is useful as a default function
    when no transformation is needed.

    PyToolz reference: toolz.functoolz.identity

    Args:
        x: Any value

    Returns:
        The same value unchanged

    Example:
        >>> identity(5)
        5
        >>> identity([1, 2, 3])
        [1, 2, 3]
    """
    pass  # Replace with your implementation


def first(seq):
    """
    Return the first element of a sequence.

    PyToolz reference: toolz.itertoolz.first

    Args:
        seq: Any iterable sequence

    Returns:
        The first element

    Example:
        >>> first([1, 2, 3])
        1
        >>> first("hello")
        'h'

    Hint: How do you safely get the first element of any iterable?
    """
    pass


def second(seq):
    """
    Return the second element of a sequence.

    PyToolz reference: toolz.itertoolz.second

    Args:
        seq: Any iterable sequence

    Returns:
        The second element

    Example:
        >>> second([1, 2, 3])
        2
        >>> second("hello")
        'e'
    """
    pass


def last(seq):
    """
    Return the last element of a sequence.

    PyToolz reference: toolz.itertoolz.last

    Args:
        seq: Any iterable sequence

    Returns:
        The last element

    Example:
        >>> last([1, 2, 3])
        3
        >>> last("hello")
        'o'

    Hint: Can you do this without converting the entire iterable to a list?
    """
    pass


def nth(n, seq):
    """
    Return the nth element of a sequence (0-indexed).

    PyToolz reference: toolz.itertoolz.nth

    Args:
        n: Index of element to retrieve (0-based)
        seq: Any iterable sequence

    Returns:
        The element at position n

    Example:
        >>> nth(2, [1, 2, 3, 4, 5])
        3
        >>> nth(0, "hello")
        'h'

    Raises:
        IndexError: If n is out of bounds
    """
    pass


def count(seq):
    """
    Count the number of items in an iterable.

    Note: This exhausts the iterable! Unlike len(), this works on
    any iterable including generators.

    PyToolz reference: toolz.itertoolz.count

    Args:
        seq: Any iterable

    Returns:
        The number of items

    Example:
        >>> count([1, 2, 3])
        3
        >>> count(range(10))
        10

    Hint: You'll need to consume the entire iterable to count it.
    """
    pass


def frequencies(seq):
    """
    Count the occurrences of each unique item in a sequence.

    Returns a dictionary mapping each unique item to its count.

    PyToolz reference: toolz.itertoolz.frequencies

    Args:
        seq: Any iterable

    Returns:
        Dictionary of {item: count}

    Example:
        >>> frequencies(['a', 'b', 'a', 'c', 'b', 'a'])
        {'a': 3, 'b': 2, 'c': 1}
        >>> frequencies([1, 1, 2, 3, 2, 1])
        {1: 3, 2: 2, 3: 1}

    Hint: Build a dictionary from scratch, updating counts as you iterate.
    """
    pass


def groupby(key, seq):
    """
    Group items in a sequence by the result of a key function.

    Returns a dictionary where keys are the results of calling key(item)
    and values are lists of items that produced that key.

    PyToolz reference: toolz.itertoolz.groupby

    Args:
        key: Function to compute grouping key for each item
        seq: Iterable to group

    Returns:
        Dictionary mapping keys to lists of items

    Example:
        >>> groupby(len, ['a', 'bb', 'ccc', 'dd', 'e'])
        {1: ['a', 'e'], 2: ['bb', 'dd'], 3: ['ccc']}
        >>> groupby(lambda x: x % 2, [1, 2, 3, 4, 5])
        {1: [1, 3, 5], 0: [2, 4]}

    Hint: Similar to frequencies, but storing lists of items instead of counts.
    """
    pass


def cons(el, seq):
    """
    Prepend an element to the beginning of a sequence.

    Returns a new list with el as the first element, followed by
    all elements from seq. The original sequence is not modified.

    PyToolz reference: toolz.itertoolz.cons

    Args:
        el: Element to prepend
        seq: Sequence to prepend to

    Returns:
        New list with el at the front

    Example:
        >>> cons(1, [2, 3, 4])
        [1, 2, 3, 4]
        >>> cons('a', 'bcd')
        ['a', 'b', 'c', 'd']

    Hint: This should return a list, not a generator.
    """
    pass


def merge(*dicts):
    """
    Merge multiple dictionaries into one.

    Later dictionaries take precedence - if the same key appears
    in multiple dicts, the value from the rightmost dict wins.

    PyToolz reference: toolz.dicttoolz.merge

    Args:
        *dicts: Variable number of dictionaries to merge

    Returns:
        New dictionary with all key-value pairs

    Example:
        >>> merge({'a': 1}, {'b': 2}, {'c': 3})
        {'a': 1, 'b': 2, 'c': 3}
        >>> merge({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
        {'a': 1, 'b': 3, 'c': 4}

    Hint: Iterate through dicts and update a result dictionary.
    """
    pass
