# WhyToolz

A functional programming kata for Python - recreating PyToolz functions from scratch!

## Overview

This project challenges you to reimplement functions from the **PyToolz** library, a functional standard library for Python. By building these functions yourself, you'll learn:

- **Functional programming** patterns and principles
- Working with **sequences and iterables**
- **Higher-order functions** (functions that take/return functions)
- How popular Python libraries work under the hood
- **Immutable data structures** and pure functions
- **Generators and lazy evaluation** (advanced section)

PyToolz is used in real-world Python applications for data processing, analytics, and functional programming. Understanding how it works will make you a better Python developer!

## Getting Started

### Prerequisites

- Python 3.11+ installed
- A modern web browser (Chrome, Firefox, Safari, or Edge)
- A text editor or IDE (VS Code, PyCharm, etc.)

### Running the Tests

1. **Open the test runner in your browser:**

   Simply open `SpecRunner.html` in your web browser.

   If opening directly doesn't work, start a local server:
   ```bash
   python3 -m http.server 8000
   ```
   Then navigate to: `http://localhost:8000/SpecRunner.html`

2. **Watch the tests run!**

   The page will show all tests with green checkmarks (passing) or red X marks (failing). Initially, all tests will fail because the functions aren't implemented yet!

3. **Implement the functions:**

   Edit the appropriate part file and implement each function:
   - `src/whytoolz_part1.py` - Foundation functions (start here!)
   - `src/whytoolz_part2.py` - Sequence manipulation functions
   - `src/whytoolz_part3.py` - Functions & dictionaries
   - `src/whytoolz_advanced.py` - Advanced challenges (optional)

   Each file contains:
   - Function signatures (without type hints, for simplicity)
   - Detailed docstrings explaining what each function should do
   - Examples of expected behavior
   - Helpful hints

4. **See your progress:**

   Save your changes and refresh the browser. Watch the tests turn green as you implement each function correctly!

## Project Structure

```
python/
├── SpecRunner.html         # Browser-based test runner (open this!)
├── README.md              # This file
├── src/
│   ├── whytoolz_part1.py   # Part I: Foundation functions
│   ├── whytoolz_part2.py   # Part II: Sequence Manipulation functions
│   ├── whytoolz_part3.py   # Part III: Functions & Dictionaries
│   └── whytoolz_advanced.py# Part IV: Advanced (Optional)
├── tests/
│   ├── framework/
│   │   └── test_framework.py   # Custom test framework (don't modify)
│   ├── test_part1.py       # Part I tests
│   ├── test_part2.py       # Part II tests
│   ├── test_part3.py       # Part III tests
│   └── test_advanced.py    # Part IV tests
└── lib/
    └── styles.css          # Test runner styling
```

## Learning Path

The functions are organized into four parts with increasing difficulty:

### Part I: Foundation (10 functions)

**Focus:** Basic operations on concrete data structures (lists, dicts, values)

Functions: `identity`, `first`, `second`, `last`, `nth`, `count`, `frequencies`, `groupby`, `cons`, `merge`

**You'll learn:**
- Working with Python's indexing and slicing
- Building dictionaries from scratch
- Iterating over sequences and objects

**Start here!** These functions return concrete values (lists, dicts, numbers), making them easier to understand and debug.

### Part II: Sequence Manipulation (11 functions)

**Focus:** Working with sequences and iterables

Functions: `islice`, `drop`, `tail`, `concat`, `unique`, `partition`, `interleave`, `pluck`, `accumulate`, `sliding_window`, `take_nth`

**You'll learn:**
- Slicing and subsetting sequences
- Combining and transforming collections
- Extracting data from nested structures
- Working with any iterable (lists, strings, ranges, etc.)

**Note:** These functions return concrete lists/values, making them easier to understand and debug.

### Part III: Functions & Dictionaries (12 functions)

**Focus:** Higher-order functions and immutable dictionary operations

Functions: `pipe`, `compose`, `complement`, `do`, `memoize`, `assoc`, `dissoc`, `valmap`, `keymap`, `valfilter`, `get_in`, `update_in`

**You'll learn:**
- Function composition and chaining
- Decorators and closures
- Immutable data structure patterns
- Nested data traversal

**Level up:** These functions work with other functions as data!

### Part IV: Advanced (6 functions - Optional)

**Focus:** Generators, lazy evaluation, and advanced patterns

Functions: `take`, `iterate`, `topk`, `reduceby`, `juxt`, `curry`

**You'll learn:**
- Generators and lazy evaluation with `yield`
- Creating infinite sequences
- Memory-efficient operations on large datasets
- Using heaps for efficient algorithms
- Simultaneous grouping and reduction
- Partial function application

**Challenge yourself:** These are harder! Try them if you finish early or want extra practice.

## Tips and Tricks

### Reading the Tests

Each test includes a description of what it's testing:

```python
@runner.it("first should pull the first element from a list")
def test_first_basic():
    assert wt.first([1, 2, 3]) == 1
```

Some tests have `FILL_ME_IN` that you need to replace:

```python
assert wt.second('hello') == FILL_ME_IN  # You figure out what this should be!
```

### Understanding Error Messages

When a test fails, you'll see:
- **The test description** (what it was testing)
- **The error message** (what went wrong)
- **The stack trace** (where the error occurred)

Use these clues to debug your implementation!

### Testing Your Code Locally

You can also run tests from the command line (but they won't look as pretty):

```python
python3 tests/test_part1.py
```

### Using Type Hints

Each function includes type hints:

```python
def first(seq: Iterable[T]) -> T:
    """Return the first element of a sequence."""
    pass
```

These tell you:
- What types the function accepts (`Iterable[T]`)
- What type it returns (`T`)
- Generic types like `T` mean "any type"

Your IDE can use these hints for autocomplete and error checking!

### Understanding Generators

Generators are a key concept in Part IV (Advanced). Here's a quick primer:

**Regular function (eager):**
```python
def get_numbers():
    return [1, 2, 3, 4, 5]  # Creates entire list in memory
```

**Generator function (lazy):**
```python
def get_numbers():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5  # Produces values one at a time
```

**Why use generators?**
- Memory efficient (don't store everything at once)
- Can represent infinite sequences
- Only compute what you need

To convert a generator to a list: `list(my_generator())`

**Note:** Parts I-III use concrete lists/values. Part IV introduces generators for advanced lazy evaluation patterns.

### Common Python Patterns

**Dictionary comprehension:**
```python
{key: value * 2 for key, value in my_dict.items()}
```

**Generator expression:**
```python
(x * 2 for x in range(10))  # Like list comprehension but lazy
```

**Itertools:**
```python
from itertools import islice, chain
islice(seq, 5)  # Take first 5 items (lazy)
chain(seq1, seq2)  # Concatenate sequences (lazy)
```

## Resources

### PyToolz Documentation

Learn more about the real PyToolz library:
- **Official Docs:** https://toolz.readthedocs.io/
- **API Reference:** https://toolz.readthedocs.io/en/latest/api.html
- **GitHub:** https://github.com/pytoolz/toolz

### Python Built-ins

Some functions are similar to Python built-ins (but you'll implement them yourself!):
- **itertools:** https://docs.python.org/3/library/itertools.html
- **functools:** https://docs.python.org/3/library/functools.html

### Functional Programming in Python

- Real Python: [Functional Programming in Python](https://realpython.com/python-functional-programming/)
- Python Docs: [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)

## Objectives

By completing this project, you'll be able to:

- ✅ Implement functions using both eager and lazy evaluation
- ✅ Work confidently with iterators and generators
- ✅ Apply functional programming principles (pure functions, immutability)
- ✅ Use higher-order functions to create reusable abstractions
- ✅ Understand how popular Python libraries are built
- ✅ Debug complex iterator and generator behavior
- ✅ Recognize when to use lazy vs eager evaluation

## Extra Credit

Once you've completed the main functions:

1. **Compare your implementations** to the real PyToolz source code:
   - Visit: https://github.com/pytoolz/toolz
   - See how your solutions differ
   - Understand what optimizations they made

2. **Add your own functions:**
   - Think of other useful functions
   - Write tests for them
   - Implement them in the PyToolz style

3. **Optimize for performance:**
   - Use `timeit` to measure function speed
   - Try different implementation approaches
   - See how close you can get to the real PyToolz performance

4. **Explore CyToolz:**
   - PyToolz has a Cython-compiled version called CyToolz
   - It's much faster! Learn why: https://github.com/pytoolz/cytoolz

## Pair Programming

This project works great with a partner! Try:

- **Driver/Navigator** pattern:
  - One person types (driver)
  - One person guides (navigator)
  - Switch roles every 15-20 minutes

- **Ping Pong** pattern:
  - Person A writes a test
  - Person B makes it pass
  - Person B writes next test
  - Person A makes it pass
  - Repeat!

## Debugging Tips

### Test failing with AttributeError?
```
AttributeError: module 'whytoolz' has no attribute 'identity'
```
→ You haven't implemented that function yet, or there's a syntax error preventing the file from loading.

### Test failing with AssertionError?
```
AssertionError: Expected [1, 2, 3], but got [1, 2, 3, 4]
```
→ Your function is returning the wrong result. Check your logic!

### Generator vs List issues?
```
AssertionError: Expected <class 'list'>, but got <class 'generator'>
```
→ Parts I-III functions should return lists/concrete values. Part IV (Advanced) functions should return generators for lazy evaluation. Check which part you're in!

### Import errors?
```
ImportError: cannot import name 'identity' from 'src.whytoolz'
```
→ Make sure your function is defined at the module level, not inside another function.

## Getting Help

Stuck? Try these strategies:

1. **Read the docstring** - It explains what the function should do
2. **Look at the tests** - They show example inputs and outputs
3. **Check the hints** - Many functions have hints in their docstrings
4. **Use print statements** - Debug by printing intermediate values
5. **Google it!** - Search for "python [function name]" or "python [concept]"
6. **Read PyToolz docs** - See how the real library describes it
7. **Ask a peer** - Explain the problem out loud (rubber duck debugging!)

## Philosophy

This project emphasizes:

- **Test-Driven Development** - Tests define the requirements
- **Functional Programming** - Pure functions, immutability, composition
- **Pythonic Code** - Using Python idioms and best practices
- **Learning by Doing** - Building things to understand them

Remember: The goal isn't just to make the tests pass. It's to **understand how these functions work** and **why they're useful**!

## Acknowledgments

This project was inspired by:
- The original [Underscore.js Kata](https://github.com/mrdavidlaing/javascript-koans)
- The excellent [PyToolz library](https://github.com/pytoolz/toolz) by Matthew Rocklin
- The functional programming community

## License

This project is for educational purposes.

---

**Ready to start?** Open `src/whytoolz_part1.py` and begin with `identity`!

**Happy coding!** 🐍✨
