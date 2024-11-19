#!/bin/bash

# Check if exactly two arguments (files) are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <file1> <file2>"
    exit 1
fi

# Get the file names from the arguments
file1=$1
file2=$2

# Check if the files exist
if [ ! -f "$file1" ]; then
    echo "Error: $file1 not found!"
    exit 1
fi

if [ ! -f "$file2" ]; then
    echo "Error: $file2 not found!"
    exit 1
fi

# Compare the files using cmp
cmp --silent "$file1" "$file2"

# $? will hold the exit status of cmp command
if [ $? -eq 0 ]; then
    echo "The files are identical."
else
    echo "The files are different."
fi
