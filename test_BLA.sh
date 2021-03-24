#!/bin/bash

# This is a simple script that runs a series of tests

TEST_DIR="tests"

export OVERRIDE_DEFAULT_GRID_SIZE="1"

# The following series of tests perform unit testing of the modules that barren_land_analyis.py relies on:

rm output 2> /dev/null
python unittest_modules.py > output
cmp --silent $TEST_DIR/expected_unittest_answer output || echo "Fails on unit testing"

# The following series of tests simulate stdin and compare stdout with the expected answer:

cat $TEST_DIR/input_file_1 | python barren_land_analysis.py > output
echo -n "9600 " > answer
cmp --silent answer output || echo "Fails on input_file_1"

cat $TEST_DIR/input_file_2 | python barren_land_analysis.py > output
echo -n "116800 116800 " > answer
cmp --silent answer output || echo "Fails on input_file_2"

cat $TEST_DIR/input_file_3 | python barren_land_analysis.py > output
echo -n "22816 192608 " > answer
cmp --silent answer output || echo "Fails on input_file_3"

cat $TEST_DIR/input_file_4 | python barren_land_analysis.py > output
echo -n "8800 " > answer
cmp --silent answer output || echo "Fails on input_file_4"

cat $TEST_DIR/break_my_code_all_barren | python barren_land_analysis.py > output
echo -n "0 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_all_barren"

cat $TEST_DIR/break_my_code_1 | python barren_land_analysis.py > output
echo -n "4500 4500 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_1"

cat $TEST_DIR/break_my_code_10_barren | python barren_land_analysis.py > output
echo -n "999000 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_10_barren"

cat $TEST_DIR/break_my_code_10_large_barren | python barren_land_analysis.py > output
echo -n "450000 450000 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_10_large_barren"

cat $TEST_DIR/break_my_code_40_barren | python barren_land_analysis.py > output
echo -n "996000 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_40_barren"

cat $TEST_DIR/break_my_code_50_barren | python barren_land_analysis.py > output
echo -n "995000 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_50_barren"

cat $TEST_DIR/break_my_code_60_barren | python barren_land_analysis.py > output
echo -n "994000 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_60_barren"

cat $TEST_DIR/break_my_code_80_barren | python barren_land_analysis.py > output
echo -n "992000 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_80_barren"

cat $TEST_DIR/break_my_code_100_barren | python barren_land_analysis.py > output
echo -n "495000 495000 " > answer
cmp --silent answer output || echo "Fails on input break_my_code_100_barren"

# A little bit of cleanup
rm answer 2> /dev/null
rm output 2> /dev/null

unset OVERRIDE_DEFAULT_GRID_SIZE