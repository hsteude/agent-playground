#!/bin/bash

# Simple math functions for smoke testing
# add: Adds two numbers and returns the sum

add() {
    local a=$1
    local b=$2
    echo $((a + b))
}

