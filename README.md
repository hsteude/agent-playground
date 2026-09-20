# Agent Playground - Bash Math Functions Smoke Test

A lightweight smoke test demonstrating Git HTTPS clone, branch creation, and Bash function testing with shell assertions.

## Implementation

### src/math.sh
Provides simple math utility functions:
- `add(a, b)`: Returns the sum of two numbers (integers)

### tests/test_math.sh
Comprehensive test suite for math functions using shell assertions:
- Tests positive number addition
- Tests negative number addition
- Tests mixed sign addition
- Tests zero and edge cases
- Exits with code 1 on any assertion failure
- Exits with code 0 on all tests passing

## Usage

### Run tests:
```bash
bash tests/test_math.sh
```

### Check syntax:
```bash
bash -n src/math.sh
bash -n tests/test_math.sh
```

## Smoke Test Details

This branch (`agent/haiku-git-https-smoke`) was created to validate:
1. Git HTTPS connectivity without custom authentication setup
2. Branch creation and management
3. Bash script authoring with assertions
4. Automated test execution
5. Git commit and push workflow
