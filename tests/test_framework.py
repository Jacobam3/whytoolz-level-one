"""
Custom test framework for WhyToolz - Browser-based Python testing
Designed to work with PyScript and provide visual test feedback
"""

from typing import Callable, Any, List, Dict
import traceback


class TestRunner:
    """Lightweight test runner for browser-based testing, similar to Mocha/Chai"""

    def __init__(self):
        self.test_suites: List[Dict[str, Any]] = []
        self.current_suite = None
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
                'passed': 0,
                'failed': 0
            }
            self.test_suites.append(suite)
            self.current_suite = suite

            # Execute the function to register its tests
            func()

            self.current_suite = None
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
            self.current_suite['tests'].append(test)
            return func
        return decorator

    def run(self):
        """Execute all registered tests"""
        self.total_passed = 0
        self.total_failed = 0
        self.total_tests = 0

        for suite in self.test_suites:
            suite['passed'] = 0
            suite['failed'] = 0

            for test in suite['tests']:
                self.total_tests += 1
                try:
                    test['func']()
                    test['status'] = 'passed'
                    suite['passed'] += 1
                    self.total_passed += 1
                except AssertionError as e:
                    test['status'] = 'failed'
                    test['error'] = str(e)
                    test['error_trace'] = traceback.format_exc()
                    suite['failed'] += 1
                    self.total_failed += 1
                except Exception as e:
                    test['status'] = 'error'
                    test['error'] = f"{type(e).__name__}: {str(e)}"
                    test['error_trace'] = traceback.format_exc()
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
        for suite in self.test_suites:
            suite_class = "suite-pass" if suite['failed'] == 0 else "suite-fail"
            html_parts.append(f'''
            <div class="test-suite {suite_class}">
                <h3 class="suite-title">{suite['description']}</h3>
                <div class="suite-stats">
                    {suite['passed']} passing, {suite['failed']} failing
                </div>
                <ul class="test-list">
            ''')

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

            html_parts.append('</ul></div>')

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
