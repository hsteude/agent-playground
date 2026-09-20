#!/bin/bash

# Test suite for math functions
set -e

source "$(dirname "$0")/../src/math.sh"

# Helper function for assertions
assert_equals() {
    local expected=$1
    local actual=$2
    local test_name=$3
    
    if [ "$expected" -eq "$actual" ]; then
        echo "✓ PASS: $test_name (expected: $expected, got: $actual)"
    else
        echo "✗ FAIL: $test_name (expected: $expected, got: $actual)"
        exit 1
    fi
}

echo "Running math.sh test suite..."
echo "=============================="

# Test positive numbers
result=$(add 5 3)
assert_equals 8 "$result" "add positive numbers (5 + 3 = 8)"

# Test negative numbers
result=$(add -5 -3)
assert_equals -8 "$result" "add negative numbers (-5 + -3 = -8)"

# Test mixed positive and negative
result=$(add 10 -4)
assert_equals 6 "$result" "add mixed signs (10 + -4 = 6)"

# Test zero
result=$(add 0 0)
assert_equals 0 "$result" "add zeros (0 + 0 = 0)"

# Test with zero
result=$(add 5 0)
assert_equals 5 "$result" "add with zero (5 + 0 = 5)"

# Test negative plus positive resulting in negative
result=$(add -10 3)
assert_equals -7 "$result" "add mixed signs negative result (-10 + 3 = -7)"

echo "=============================="
echo "All tests passed!"
exit 0
