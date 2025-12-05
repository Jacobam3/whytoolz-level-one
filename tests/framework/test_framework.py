"""
Custom test framework for WhyToolz - Browser-based Python testing
Designed to work with PyScript and provide visual test feedback
"""

from typing import Callable, Any, List, Dict
import traceback
import inspect
import re


class TestRunner:
    """Lightweight test runner for browser-based testing, similar to Mocha/Chai"""

    def __init__(self):
        self.test_suites: List[Dict[str, Any]] = []
        self.current_suite = None
        self.current_subsuite = None
        self.total_passed = 0
        self.total_failed = 0
        self.total_tests = 0

    def describe(self, description: str):
        """
        Create a test suite (group of related tests)
        Usage:
            runner = TestRunner()

            @runner.describe("My Feature")
            def test_my_feature():
                # tests go here
                pass
        """
        def decorator(func: Callable):
            suite = {
                'description': description,
                'tests': [],
                'subsuites': [],
                'passed': 0,
                'failed': 0
            }
            self.test_suites.append(suite)
            self.current_suite = suite
            self.current_subsuite = None

            # Execute the function to register its tests
            func()

            self.current_suite = None
            return func
        return decorator

    def subsuite(self, description: str):
        """
        Create a test subsuite within the current suite (for grouping by function)
        Usage:
            @runner.subsuite("identity function")
            def test_identity():
                # tests for identity go here
                pass
        """
        def decorator(func: Callable):
            if self.current_suite is None:
                raise RuntimeError("subsuite() must be called inside a describe() block")

            subsuite = {
                'description': description,
                'tests': [],
                'passed': 0,
                'failed': 0
            }
            self.current_suite['subsuites'].append(subsuite)
            self.current_subsuite = subsuite

            # Execute the function to register its tests
            func()

            self.current_subsuite = None
            return func
        return decorator

    def it(self, description: str):
        """
        Define an individual test case
        Usage:
            @runner.it("should do something")
            def test_something():
                assert True
        """
        def decorator(func: Callable):
            if self.current_suite is None:
                raise RuntimeError("it() must be called inside a describe() block")

            test = {
                'description': description,
                'func': func,
                'status': None,
                'error': None,
                'error_trace': None
            }

            # Add to subsuite if one is active, otherwise add to main suite
            if self.current_subsuite is not None:
                self.current_subsuite['tests'].append(test)
            else:
                self.current_suite['tests'].append(test)
            return func
        return decorator

    def _extract_assertion_info(self, test_func: Callable, error: AssertionError, tb_str: str) -> str:
        """
        Extract meaningful information from an assertion failure.

        Parses the traceback to find the assertion line and evaluates it to show
        what was expected vs what was actually returned.
        """
        error_msg = str(error)

        # If the AssertionError already has a message, use it as is
        if error_msg:
            return error_msg

        # Try to extract the assertion line from the traceback and evaluate it
        try:
            # Parse traceback to extract the assertion line
            tb_lines = tb_str.strip().split('\n')
            assertion_line = None

            # Look through traceback for the actual line that failed
            for i, line in enumerate(tb_lines):
                if 'assert ' in line and not line.strip().startswith('#'):
                    assertion_line = line.strip()
                    break

            # Try to get source code for more detail
            if not assertion_line:
                try:
                    source_lines = inspect.getsourcelines(test_func)[0]
                    # Find assertion line in source
                    for src_line in source_lines:
                        if 'assert' in src_line:
                            assertion_line = src_line.strip()
                            break
                except (OSError, TypeError):
                    pass

            if assertion_line:
                # Try to extract the comparison operator and operands
                # Handle ==, !=, >, <, >=, <=, is, is not, in, not in
                comparison_patterns = [
                    (r'assert\s+(.+?)\s*(==|!=|>=|<=|>|<)\s*(.+)$', 'comparison'),
                    (r'assert\s+(.+?)\s*(is\s+not|is)\s+(.+)$', 'identity'),
                    (r'assert\s+(.+?)\s*(in|not\s+in)\s+(.+)$', 'membership'),
                ]

                for pattern, op_type in comparison_patterns:
                    match = re.match(pattern, assertion_line)
                    if match:
                        try:
                            left_expr = match.group(1).strip()
                            operator = match.group(2).strip()
                            right_expr = match.group(3).strip()

                            # Try to evaluate the left side (the function call)
                            # Use the test function's globals and locals
                            test_locals = {}
                            test_globals = test_func.__globals__.copy() if hasattr(test_func, '__globals__') else {}

                            # Execute the left side to get the actual value
                            try:
                                actual = eval(left_expr, test_globals, test_locals)
                                expected_str = right_expr

                                # Clean up the left expression for display (remove 'wt.' prefix)
                                clean_left = left_expr.replace('wt.', '')

                                # Format output based on operator type
                                if op_type == 'comparison':
                                    return f"Expected: {expected_str}\nActual: {repr(actual)}\n\nAssertion: {clean_left} {operator} {expected_str}"
                                elif op_type == 'identity':
                                    return f"Expected: {expected_str}\nActual: {repr(actual)}\n\nAssertion: {clean_left} {operator} {expected_str}"
                                elif op_type == 'membership':
                                    return f"Expected: {repr(actual)} to be {operator} {expected_str}\n\nAssertion: {clean_left} {operator} {expected_str}"
                            except Exception:
                                # If evaluation fails, just show the assertion line
                                return f"Assertion failed:\n  {assertion_line}"
                        except Exception:
                            pass

                # If we couldn't parse it as a comparison, just show the assertion line
                return f"Assertion failed:\n  {assertion_line}"

        except Exception:
            # If anything goes wrong with extraction, just use generic message
            pass

        # Fallback message
        return "Assertion failed"

    def run(self):
        """Execute all registered tests"""
        self.total_passed = 0
        self.total_failed = 0
        self.total_tests = 0

        for suite in self.test_suites:
            suite['passed'] = 0
            suite['failed'] = 0

            # Run tests at suite level
            for test in suite['tests']:
                self.total_tests += 1
                try:
                    test['func']()
                    test['status'] = 'passed'
                    suite['passed'] += 1
                    self.total_passed += 1
                except AssertionError as e:
                    test['status'] = 'failed'
                    tb_str = traceback.format_exc()
                    # Try to extract enhanced error message
                    test['error'] = self._extract_assertion_info(test['func'], e, tb_str)
                    test['error_trace'] = tb_str
                    suite['failed'] += 1
                    self.total_failed += 1
                except Exception as e:
                    test['status'] = 'error'
                    test['error'] = f"{type(e).__name__}: {str(e)}"
                    test['error_trace'] = traceback.format_exc()
                    suite['failed'] += 1
                    self.total_failed += 1

            # Run tests in subsuites
            for subsuite in suite['subsuites']:
                subsuite['passed'] = 0
                subsuite['failed'] = 0

                for test in subsuite['tests']:
                    self.total_tests += 1
                    try:
                        test['func']()
                        test['status'] = 'passed'
                        subsuite['passed'] += 1
                        suite['passed'] += 1
                        self.total_passed += 1
                    except AssertionError as e:
                        test['status'] = 'failed'
                        tb_str = traceback.format_exc()
                        # Try to extract enhanced error message
                        test['error'] = self._extract_assertion_info(test['func'], e, tb_str)
                        test['error_trace'] = tb_str
                        subsuite['failed'] += 1
                        suite['failed'] += 1
                        self.total_failed += 1
                    except Exception as e:
                        test['status'] = 'error'
                        test['error'] = f"{type(e).__name__}: {str(e)}"
                        test['error_trace'] = traceback.format_exc()
                        subsuite['failed'] += 1
                        suite['failed'] += 1
                        self.total_failed += 1

    def get_results(self) -> Dict[str, Any]:
        """Get test results as a dictionary"""
        return {
            'suites': self.test_suites,
            'total_passed': self.total_passed,
            'total_failed': self.total_failed,
            'total_tests': self.total_tests
        }

    def display_results(self, element_id: str = "test-results"):
        """Render test results to the DOM (PyScript only)"""
        try:
            from js import document

            container = document.getElementById(element_id)
            if not container:
                print(f"Error: Element with id '{element_id}' not found")
                return

            html = self._generate_html()
            container.innerHTML = html

        except ImportError:
            # Not running in PyScript, print to console instead
            self._print_results()

    def _generate_html(self) -> str:
        """Generate HTML for test results"""
        html_parts = []

        # Summary stats
        pass_rate = (self.total_passed / self.total_tests * 100) if self.total_tests > 0 else 0
        summary_class = "summary-pass" if self.total_failed == 0 else "summary-fail"

        html_parts.append(f'''
        <div class="test-summary {summary_class}">
            <h2>Test Results</h2>
            <div class="stats">
                <span class="stat-passed">{self.total_passed} passing</span>
                <span class="stat-failed">{self.total_failed} failing</span>
                <span class="stat-total">({self.total_tests} total)</span>
                <span class="stat-rate">{pass_rate:.1f}% pass rate</span>
            </div>
        </div>
        ''')

        # Individual test suites
        for suite_idx, suite in enumerate(self.test_suites):
            suite_class = "suite-pass" if suite['failed'] == 0 else "suite-fail"
            is_all_passing = suite['failed'] == 0

            # Determine initial state: collapse if all passing, expand if any failing
            initial_state = "collapsed" if is_all_passing else "expanded"
            arrow = "▶" if is_all_passing else "▼"

            html_parts.append(f'''
            <div class="test-suite {suite_class}">
                <button class="suite-toggle {initial_state}" data-suite-id="suite-{suite_idx}" onclick="toggleSuite('suite-{suite_idx}')">
                    <span class="toggle-arrow">{arrow}</span>
                    <h3 class="suite-title-inline">{suite['description']}</h3>
                    <span class="suite-badge">{suite['passed']}/{suite['passed'] + suite['failed']} passing</span>
                </button>
                <div class="suite-content {initial_state}" id="suite-{suite_idx}">
                    <div class="suite-stats">
                        {suite['passed']} passing, {suite['failed']} failing
                    </div>
            ''')

            # Top-level tests in the suite
            if suite['tests']:
                html_parts.append('<ul class="test-list">')
                for test in suite['tests']:
                    status_icon = "✓" if test['status'] == 'passed' else "✗"
                    status_class = f"test-{test['status']}"

                    html_parts.append(f'''
                    <li class="test-item {status_class}">
                        <span class="test-icon">{status_icon}</span>
                        <span class="test-description">{test['description']}</span>
                    ''')

                    if test['status'] in ['failed', 'error']:
                        html_parts.append(f'''
                        <div class="test-error">
                            <div class="error-message">{test['error']}</div>
                            <pre class="error-trace">{test['error_trace']}</pre>
                        </div>
                        ''')

                    html_parts.append('</li>')
                html_parts.append('</ul>')

            # Subsuites (function groupings)
            for subsuite_idx, subsuite in enumerate(suite['subsuites']):
                subsuite_class = "subsuite-pass" if subsuite['failed'] == 0 else "subsuite-fail"
                is_subsuite_passing = subsuite['failed'] == 0
                subsuite_initial_state = "collapsed" if is_subsuite_passing else "expanded"
                subsuite_arrow = "▶" if is_subsuite_passing else "▼"

                html_parts.append(f'''
                    <div class="test-subsuite {subsuite_class}">
                        <button class="subsuite-toggle {subsuite_initial_state}" data-subsuite-id="subsuite-{suite_idx}-{subsuite_idx}" onclick="toggleSuite('subsuite-{suite_idx}-{subsuite_idx}')">
                            <span class="toggle-arrow">{subsuite_arrow}</span>
                            <h4 class="subsuite-title-inline">{subsuite['description']}</h4>
                            <span class="subsuite-badge">{subsuite['passed']}/{subsuite['passed'] + subsuite['failed']} passing</span>
                        </button>
                        <div class="subsuite-content {subsuite_initial_state}" id="subsuite-{suite_idx}-{subsuite_idx}">
                            <ul class="test-list">
                ''')

                for test in subsuite['tests']:
                    status_icon = "✓" if test['status'] == 'passed' else "✗"
                    status_class = f"test-{test['status']}"

                    html_parts.append(f'''
                        <li class="test-item {status_class}">
                            <span class="test-icon">{status_icon}</span>
                            <span class="test-description">{test['description']}</span>
                        ''')

                    if test['status'] in ['failed', 'error']:
                        html_parts.append(f'''
                        <div class="test-error">
                            <div class="error-message">{test['error']}</div>
                            <pre class="error-trace">{test['error_trace']}</pre>
                        </div>
                        ''')

                    html_parts.append('</li>')

                html_parts.append('''
                            </ul>
                        </div>
                    </div>
                ''')

            html_parts.append('</div></div>')

        return ''.join(html_parts)

    def _print_results(self):
        """Print test results to console (fallback for non-browser)"""
        print("\n" + "="*70)
        print(f"TEST RESULTS: {self.total_passed}/{self.total_tests} passed")
        print("="*70)

        for suite in self.test_suites:
            print(f"\n{suite['description']}")
            print("-" * 70)

            for test in suite['tests']:
                status = "✓" if test['status'] == 'passed' else "✗"
                print(f"  {status} {test['description']}")

                if test['status'] in ['failed', 'error']:
                    print(f"    Error: {test['error']}")
                    if test['error_trace']:
                        print(f"    {test['error_trace']}")


def expect(actual: Any) -> 'Assertion':
    """
    Create an assertion object for testing (Chai-style, but Pythonic)

    Usage:
        expect(value).to_equal(5)
        expect(result).to_be_truthy()
    """
    return Assertion(actual)


class Assertion:
    """Provides chainable assertions similar to Chai, but using Python idioms"""

    def __init__(self, actual: Any):
        self.actual = actual

    def to_equal(self, expected: Any):
        """Assert that actual == expected"""
        assert self.actual == expected, \
            f"Expected {repr(expected)}, but got {repr(self.actual)}"
        return self

    def to_be(self, expected: Any):
        """Assert that actual is expected (identity check)"""
        assert self.actual is expected, \
            f"Expected {repr(expected)} (same object), but got {repr(self.actual)}"
        return self

    def to_be_truthy(self):
        """Assert that actual is truthy"""
        assert bool(self.actual), \
            f"Expected truthy value, but got {repr(self.actual)}"
        return self

    def to_be_falsy(self):
        """Assert that actual is falsy"""
        assert not bool(self.actual), \
            f"Expected falsy value, but got {repr(self.actual)}"
        return self

    def to_be_none(self):
        """Assert that actual is None"""
        assert self.actual is None, \
            f"Expected None, but got {repr(self.actual)}"
        return self

    def to_not_be_none(self):
        """Assert that actual is not None"""
        assert self.actual is not None, \
            f"Expected non-None value, but got None"
        return self

    def to_contain(self, item: Any):
        """Assert that item is in actual"""
        assert item in self.actual, \
            f"Expected {repr(self.actual)} to contain {repr(item)}"
        return self

    def to_have_length(self, length: int):
        """Assert that actual has specified length"""
        actual_length = len(self.actual)
        assert actual_length == length, \
            f"Expected length {length}, but got {actual_length}"
        return self

    def to_be_instance_of(self, cls: type):
        """Assert that actual is an instance of cls"""
        assert isinstance(self.actual, cls), \
            f"Expected instance of {cls.__name__}, but got {type(self.actual).__name__}"
        return self

    def to_raise(self, exception_type: type = Exception):
        """
        Assert that calling actual() raises specified exception
        Note: actual should be a callable
        """
        try:
            self.actual()
            raise AssertionError(f"Expected {exception_type.__name__} to be raised, but nothing was raised")
        except exception_type:
            pass  # Expected exception was raised
        except Exception as e:
            raise AssertionError(
                f"Expected {exception_type.__name__} to be raised, "
                f"but {type(e).__name__} was raised instead"
            )
        return self


# Global test runner instance (similar to how Mocha works)
_global_runner = None


def create_runner() -> TestRunner:
    """Create and return a new TestRunner instance"""
    global _global_runner
    _global_runner = TestRunner()
    return _global_runner


def get_runner() -> TestRunner:
    """Get the global test runner instance"""
    return _global_runner


def run_all_tests(test_modules: List[Any]) -> TestRunner:
    """
    Import and run all test modules

    Usage:
        from tests import test_part1, test_part2
        runner = run_all_tests([test_part1, test_part2])
        runner.display_results()
    """
    runner = create_runner()

    # Import all test modules (they will register themselves)
    for module in test_modules:
        # Module imports register tests via decorators
        pass

    # Run all tests
    runner.run()

    return runner
