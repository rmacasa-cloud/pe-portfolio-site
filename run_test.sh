#!/bin/bash

# Discover and run every test file under the tests/ directory.
# -v gives verbose output so you can see each individual test name and result.
python -m unittest discover -v tests