"""
Test runner script for the Sports Booking Management System.

This script provides convenient commands to run tests with various configurations.
"""

import sys
import subprocess


def run_command(cmd):
    """Run a shell command and return the result."""
    print(f"\n{'=' * 60}")
    print(f"Running: {cmd}")
    print(f"{'=' * 60}\n")
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def main():
    """Main test runner with various options."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <option>")
        print("\nOptions:")
        print("  all              - Run all tests")
        print("  booking          - Run booking input service tests")
        print("  coverage         - Run tests with coverage report")
        print("  coverage-html    - Run tests with HTML coverage report")
        print("  verbose          - Run tests with verbose output")
        print("  fast             - Run tests excluding slow tests")
        print("  specific <path>  - Run specific test file or method")
        sys.exit(1)

    option = sys.argv[1].lower()

    if option == "all":
        return run_command("python -m pytest tests/")

    elif option == "booking":
        return run_command(
            "python -m pytest tests/business_logic/services/test_booking_input_service.py"
        )

    elif option == "coverage":
        return run_command(
            "python -m pytest tests/ --cov=business_logic --cov=persistence --cov=presentation --cov-report=term-missing"
        )

    elif option == "coverage-html":
        result = run_command(
            "python -m pytest tests/ --cov=business_logic --cov=persistence --cov=presentation --cov-report=html"
        )
        if result == 0:
            print("\n✅ Coverage report generated in htmlcov/index.html")
        return result

    elif option == "verbose":
        return run_command("python -m pytest tests/ -vv")

    elif option == "fast":
        return run_command("python -m pytest tests/ -m 'not slow'")

    elif option == "specific" and len(sys.argv) > 2:
        test_path = sys.argv[2]
        return run_command(f"python -m pytest {test_path}")

    else:
        print(f"❌ Unknown option: {option}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
