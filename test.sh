#!/bin/bash

declare file="test_results"
declare regex=" tests, 0 errors, 0 failures, 0 skipped"

# Build, runs tests and store results
. /opt/ros/galactic/setup.bash
colcon build
colcon test
exit 1
