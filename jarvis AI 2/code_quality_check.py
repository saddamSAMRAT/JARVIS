import os
import sys
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Running: {command}")
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running {command}: {e}")
        return 1

def main():
    # Directories to check
    check_dirs = [
        'backend',
        'frontend/src'
    ]

    # Code quality checks
    checks = [
        # Python linting
        f"python -m pylint {' '.join(check_dirs)}",
        
        # Python type checking
        f"python -m mypy {' '.join(check_dirs)}",
        
        # Code formatting
        f"python -m black --check {' '.join(check_dirs)}",
        
        # JavaScript/React checks
        "npm run lint"  # Assumes this is defined in package.json
    ]

    # Run checks
    failed_checks = []
    for check in checks:
        result = run_command(check)
        if result != 0:
            failed_checks.append(check)

    # Report results
    if failed_checks:
        print("\n❌ Code Quality Checks Failed:")
        for failed in failed_checks:
            print(f" - {failed}")
        sys.exit(1)
    else:
        print("\n✅ All Code Quality Checks Passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
